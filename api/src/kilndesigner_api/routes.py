"""The API's routes: designs, their versions, and builds."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator
from pathlib import Path, PurePath
from typing import Annotated, Any

import yaml
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import FileResponse
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from kilndesigner import Kiln, dump_design, parse_design, results
from kilndesigner.build import build_key, design_document
from kilndesigner.castable import CastableError, ingredients, mix_analysis
from kilndesigner.cones import cone_names, cone_rates
from kilndesigner.gas import gas_data, named_model
from kilndesigner.library import alloys, materials
from kilndesigner.report import Report
from kilndesigner.results import WallHeatmap, read_summary
from kilndesigner.simulation import FiringPoint, FiringResult, SwitchOverChart
from kilndesigner.templates import templates
from kilndesigner_api import db, schemas
from kilndesigner_api.jobs import JobRunner
from kilndesigner_api.settings import Settings
from kilndesigner_api.tasks import build_dir, simulation_dir

router = APIRouter(
    prefix="/api",
    responses={422: {"model": schemas.InvalidDesign, "description": "The design is not valid"}},
)


class InvalidDesignError(Exception):
    def __init__(self, problems: list[schemas.Problem]) -> None:
        self.problems = problems


def read_design(body: schemas.DesignInput) -> tuple[Kiln, str]:
    """Validate a design, returning it with the YAML to store. A castable mix the engine can't
    work out is refused here, with where it is, rather than failing its build later."""
    try:
        if body.source is not None:
            kiln, source = parse_design(body.source), body.source
        else:
            kiln = Kiln.model_validate(body.document)
            source = dump_design(kiln)
    except yaml.YAMLError as e:
        raise InvalidDesignError([schemas.Problem(loc=[], msg=f"not valid YAML: {e}")]) from e
    except ValidationError as e:
        problems = [schemas.Problem(loc=list(p["loc"]), msg=p["msg"]) for p in e.errors()]
        raise InvalidDesignError(problems) from e  # pydantic wraps a UnitError in this too
    problems: list[schemas.Problem] = []
    known = set(materials()) | {m.id for m in kiln.castables or []}
    for face in ("walls", "floor", "roof", "door"):
        for i, layer in enumerate(getattr(kiln.lining, face) or []):
            if layer.material not in known:
                problems.append(
                    schemas.Problem(
                        loc=["lining", face, i, "material"],
                        msg=f"no material or castable called {layer.material!r}",
                    )
                )
    for i, mix in enumerate(kiln.castables or []):
        try:
            mix_analysis(kiln, mix)
        except CastableError as e:
            problems.append(schemas.Problem(loc=["castables", i], msg=str(e)))
    electric, gas = kiln.heat.electric, kiln.heat.gas
    if electric is not None and electric.alloy not in alloys():
        problems.append(
            schemas.Problem(
                loc=["heat", "electric", "alloy"], msg=f"no alloy called {electric.alloy!r}"
            )
        )
    if gas is not None and gas.burners.model is not None:
        # Named as the engine matches them: the end of a name, among the burners of that type
        kind = gas.burners.type
        if named_model(kind, gas.burners.model) is None:
            names = (
                list(gas_data()["venturi_burners"]["models"])
                if kind == "venturi"
                else [f"Ward {m}" for m in gas_data()["power_burners"]["models"]]
            )
            problems.append(
                schemas.Problem(
                    loc=["heat", "gas", "burners", "model"],
                    msg=(
                        f"no {kind} burner called {gas.burners.model!r}; the "
                        f"library has: {', '.join(names)}"
                    ),
                )
            )
    if problems:
        raise InvalidDesignError(problems)
    return kiln, source


async def _session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.sessions() as s:
        yield s


def _runner(request: Request) -> JobRunner:
    return request.app.state.runner


def _settings(request: Request) -> Settings:
    return request.app.state.settings


Session = Annotated[AsyncSession, Depends(_session)]
Runner = Annotated[JobRunner, Depends(_runner)]
AppSettings = Annotated[Settings, Depends(_settings)]


async def _load(s: AsyncSession, design_id: uuid.UUID) -> db.Design:
    design = await s.scalar(
        select(db.Design)
        .where(db.Design.id == design_id)
        .options(selectinload(db.Design.versions))
        .execution_options(populate_existing=True)  # pick up server defaults after a commit
    )
    if design is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no such design")
    return design


def _out(design: db.Design) -> schemas.Design:
    return schemas.Design(
        id=design.id,
        name=design.name,
        created_at=design.created_at,
        updated_at=design.updated_at,
        versions=[schemas.VersionSummary.model_validate(v) for v in design.versions],
        latest=schemas.Version.model_validate(design.versions[-1]),
    )


FILES_MISSING = (
    "its files are no longer in the data folder (it was cleared, or another setup shares this "
    "database)"
)


async def _get_build(s: AsyncSession, settings: Settings, key: str) -> db.Build | None:
    """A build, marked failed if it finished but its files have gone, so it can be built again."""
    build = await s.get(db.Build, key)
    if build is not None and build.status == db.BuildStatus.done:
        folder = build_dir(settings.data_dir, key)
        if not all((folder / name).is_file() for name in build.files):
            build.status, build.error = db.BuildStatus.failed, FILES_MISSING
            await s.commit()
    return build


def _new_version(design: db.Design, number: int, kiln: Kiln, source: str) -> db.DesignVersion:
    return db.DesignVersion(
        design=design,
        number=number,
        schema_version=kiln.schema_version,
        document=design_document(kiln),
        source=source,
        build_key=build_key(kiln),
    )


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/schema")
async def design_schema() -> dict[str, Any]:
    """The design file's JSON Schema: the generated forms are built from it."""
    return Kiln.model_json_schema(by_alias=True)


@router.get("/templates")
async def list_templates() -> list[schemas.Template]:
    """The kinds of kiln a design can start from, each a complete design."""
    return [
        schemas.Template(
            id=t.id,
            title=t.title,
            description=t.description,
            document=design_document(t.kiln),
            source=t.source,
        )
        for t in templates()
    ]


@router.get("/library")
async def library() -> schemas.Library:
    """What the forms offer: the materials library, alloys, cones and burners."""
    gas = gas_data()
    burners = [
        schemas.LibraryEntry(id=name, name=f"{name} (venturi)")
        for name in gas["venturi_burners"]["models"]
    ] + [
        schemas.LibraryEntry(id=name, name=f"Ward {name} (power)")
        for name in gas["power_burners"]["models"]
    ]
    return schemas.Library(
        materials=[
            schemas.LibraryMaterial(
                id=m.id, name=m.name, kind=m.kind, max_service=m.max_service, density=m.density
            )
            for m in materials().values()
        ],
        ingredients=[
            schemas.LibraryIngredient(
                id=i.id, name=i.name, role=i.role, needs_density=i.density is None
            )
            for i in ingredients().values()
        ],
        alloys=[schemas.LibraryEntry(id=a.id, name=a.name) for a in alloys().values()],
        cones=list(cone_names()),
        cone_rates={c: list(cone_rates(c)) for c in cone_names()},
        burners=burners,
    )


@router.post("/designs/check")
async def check_design(body: schemas.DesignInput) -> schemas.CheckedDesign:
    """Check a design without saving it, and return it as both a document and YAML: the form and
    the YAML tab trade the design through here."""
    kiln, source = read_design(body)
    return schemas.CheckedDesign(document=design_document(kiln), source=source)


@router.get("/designs")
async def list_designs(s: Session) -> list[schemas.DesignSummary]:
    rows = await s.scalars(select(db.Design).order_by(db.Design.updated_at.desc()))
    return [schemas.DesignSummary.model_validate(d) for d in rows]


@router.post("/designs", status_code=status.HTTP_201_CREATED)
async def create_design(body: schemas.DesignInput, s: Session) -> schemas.Design:
    kiln, source = read_design(body)
    design = db.Design(name=kiln.name)
    s.add(_new_version(design, 1, kiln, source))
    await s.commit()
    return _out(await _load(s, design.id))


@router.get("/designs/{design_id}")
async def get_design(design_id: uuid.UUID, s: Session) -> schemas.Design:
    return _out(await _load(s, design_id))


@router.delete("/designs/{design_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_design(design_id: uuid.UUID, s: Session) -> None:
    await s.delete(await _load(s, design_id))
    await s.commit()


@router.post("/designs/{design_id}/versions")
async def save_version(
    design_id: uuid.UUID, body: schemas.DesignInput, s: Session
) -> schemas.Design:
    """Save a new version. Saving the latest version again, unchanged, adds nothing."""
    kiln, source = read_design(body)
    design = await _load(s, design_id)
    latest = design.versions[-1]
    if source == latest.source:
        return _out(design)
    design.name, design.updated_at = kiln.name, db.now()
    s.add(_new_version(design, latest.number + 1, kiln, source))
    await s.commit()
    return _out(await _load(s, design_id))


@router.get("/designs/{design_id}/versions/{number}")
async def get_version(design_id: uuid.UUID, number: int, s: Session) -> schemas.Version:
    version = await s.scalar(
        select(db.DesignVersion).where(
            db.DesignVersion.design_id == design_id, db.DesignVersion.number == number
        )
    )
    if version is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no such version")
    return schemas.Version.model_validate(version)


@router.post("/builds/{key}", status_code=status.HTTP_202_ACCEPTED)
async def start_build(key: str, s: Session, runner: Runner, settings: AppSettings) -> schemas.Build:
    """Build a design version by its build key. A build already made is returned as it is."""
    known = await s.scalar(
        select(func.count()).select_from(db.DesignVersion).where(db.DesignVersion.build_key == key)
    )
    if not known:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no design version has this build key")
    build = await _get_build(s, settings, key)
    if build is None:
        build = db.Build(key=key, status=db.BuildStatus.queued, files=[], notes=[])
        s.add(build)
    elif build.status == db.BuildStatus.failed:
        build.status, build.error, build.finished_at = db.BuildStatus.queued, None, None
    else:
        return schemas.Build.model_validate(build)
    await s.commit()
    await s.refresh(build)
    queued = schemas.Build.model_validate(build)
    await runner.submit_build(key)
    return queued


@router.get("/builds/{key}")
async def get_build(key: str, s: Session, settings: AppSettings) -> schemas.Build:
    build = await _get_build(s, settings, key)
    if build is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not built")
    return schemas.Build.model_validate(build)


@router.get("/builds/{key}/report")
async def build_report(key: str, s: Session, settings: AppSettings) -> Report:
    """The build's report, with its working and findings."""
    build = await _get_build(s, settings, key)
    if build is None or build.status != db.BuildStatus.done or "report.json" not in build.files:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no report")
    path = build_dir(settings.data_dir, key) / "report.json"
    return Report.model_validate_json(path.read_bytes())


async def _done_simulation(s: AsyncSession, settings: Settings, key: str) -> Path:
    """The folder of a finished simulation, or 404."""
    sim = await s.get(db.Simulation, key)
    folder = simulation_dir(settings.data_dir, key)
    if sim is None or sim.status != db.BuildStatus.done or not (folder / "firing.json").is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no finished simulation")
    return folder


@router.post("/simulations/{key}", status_code=status.HTTP_202_ACCEPTED)
async def start_simulation(
    key: str, s: Session, runner: Runner, settings: AppSettings
) -> schemas.Simulation:
    """Simulate a firing of a design version, by its build key. A finished run is returned."""
    known = await s.scalar(
        select(func.count()).select_from(db.DesignVersion).where(db.DesignVersion.build_key == key)
    )
    if not known:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no design version has this build key")
    sim = await s.get(db.Simulation, key)
    if sim is not None and sim.status == db.BuildStatus.done:
        if (simulation_dir(settings.data_dir, key) / "firing.json").is_file():
            return schemas.Simulation.model_validate(sim)
        sim.status = db.BuildStatus.failed  # its files have gone: run it again
    if sim is None:
        sim = db.Simulation(key=key)
        s.add(sim)
    elif sim.status == db.BuildStatus.failed:
        sim.status, sim.error, sim.finished_at = db.BuildStatus.queued, None, None
    else:
        return schemas.Simulation.model_validate(sim)
    await s.commit()
    await s.refresh(sim)
    queued = schemas.Simulation.model_validate(sim)
    await runner.submit_simulation(key)
    return queued


@router.get("/simulations/{key}")
async def get_simulation(key: str, s: Session) -> schemas.Simulation:
    sim = await s.get(db.Simulation, key)
    if sim is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "not simulated")
    return schemas.Simulation.model_validate(sim)


@router.get("/simulations/{key}/result")
async def simulation_result(key: str, s: Session, settings: AppSettings) -> FiringResult:
    """The firing's summary, with its working and findings (every step's point is included)."""
    return read_summary(await _done_simulation(s, settings, key))


@router.get("/simulations/{key}/series")
async def simulation_series(
    key: str,
    s: Session,
    settings: AppSettings,
    max_points: Annotated[int, Query(ge=2, le=20_000)] = 500,
) -> list[FiringPoint]:
    """The firing through time, read from Parquet with DuckDB, thinned to ``max_points``."""
    return results.series(await _done_simulation(s, settings, key), max_points)


@router.get("/simulations/{key}/heatmap")
async def simulation_heatmap(
    key: str,
    s: Session,
    settings: AppSettings,
    max_times: Annotated[int, Query(ge=2, le=2_000)] = 200,
) -> WallHeatmap:
    """Each wall's temperatures through its thickness and through time, for the 3D heatmap."""
    return results.heatmap(await _done_simulation(s, settings, key), max_times)


@router.get("/simulations/{key}/switchover")
async def simulation_switchover(key: str, s: Session, settings: AppSettings) -> SwitchOverChart:
    """A hybrid's firing time and cost against its hand-over temperature."""
    path = await _done_simulation(s, settings, key) / "switchover.json"
    if not path.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no switch-over chart for this kiln")
    return SwitchOverChart.model_validate_json(path.read_bytes())


@router.get("/builds/{key}/files/{name:path}", response_class=FileResponse)
async def build_file(key: str, name: str, s: Session, settings: AppSettings) -> FileResponse:
    """A file the build wrote, by its path in the build: ``plans.pdf``, ``drawings/view-1.svg``.
    Only the paths the build recorded can be fetched."""
    build = await _get_build(s, settings, key)
    if build is None or build.status != db.BuildStatus.done or name not in build.files:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "no such file")
    return FileResponse(build_dir(settings.data_dir, key) / name, filename=PurePath(name).name)
