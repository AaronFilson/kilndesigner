"""Olsen's kilns (*The Kiln Book*, 4th ed.): real kilns, built and fired. Each is a design in
``examples/olsen``, and the engine must build every one without an error. A warning that remains
says something true about the kiln as built (a brick fired past its rating); each is listed here
with why, so a new warning on a working kiln fails until someone looks at it.
"""

from pathlib import Path

import pytest

from kilndesigner import load_design
from kilndesigner.build import design_document
from kilndesigner.report import design_report

OLSEN = Path(__file__).parents[2] / "examples" / "olsen"
KILNS = sorted(OLSEN.glob("*.yaml"))

K23_AT_CONE_10 = (
    "2300 °F insulating brick at cone 10, as Olsen built the fast-fire kiln (p.140); past its "
    "rating it shrinks and wears faster (p.25–26: K-23 is for cone 6)"
)

WARNED: dict[str, dict[str, str]] = {
    "fast-fire": {"heatloss.service": K23_AT_CONE_10},
    "fast-fire-anderson": {"heatloss.service": K23_AT_CONE_10},
    "blakebrough-tasmania": {
        "hardware.flue": "the book's 9 × 6 in flue into the chimney (p.148) is under 1 in² per "
        "7000 BTU/hr (p.236) of the input the engine sizes for the 68 ft³ fibre box; the book "
        "gives no burner rating, so this holds if the burners were that large",
    },
    "chappell-domura": {
        "fire.grate": "one 12 × 12 in chimney draws both the salt kiln and the two-chamber kiln "
        "beside it (p.126), so it is large for the salt kiln's firebox alone (its size not "
        "printed: 9 in assumed, as the two-chamber kiln's in the same drawing)",
    },
    "breda-bottle": {
        "masonry.thickness": "the book's 2 ft wall (p.166) isn't whole 9 and 4½ in rings, so the "
        "round wall isn't counted in brick",
    },
    "kenzan-muffle": {
        "masonry.thickness": "the 4 in wall, floor and roof as built aren't whole bricks",
    },
    "bowen-mountain": {
        "frame.post": "with the rods about 18 in over the crown (the user's estimate), "
        "the corner posts bend past HarbisonWalker's 12,000 psi, though within AISC's strength",
    },
    "ninodaguia": {
        "masonry.thickness": "the 15½ in wall isn't whole 9 and 4½ in rings",
    },
    "tobe": {
        "heatloss.rayleigh": "its roof, about 25 × 73 ft, is past the Rayleigh number its "
        "convection correlation is checked to (thermal-properties.md §5), so that face's loss is "
        "less certain",
    },
}
"""The warnings each kiln raises, by check, and why they are right to stay."""


def _family(check_id: str) -> str:
    """'heatloss.service.roof.1' and 'heatloss.service.roof.1-2' are both 'heatloss.service'."""
    return ".".join(check_id.split("-")[0].split(".")[:2])


def test_every_kiln_is_there() -> None:
    """Every kiln the book sizes (examples/olsen/README.md lists them, and the ones it can't)."""
    assert len(KILNS) == 53
    assert set(WARNED) <= {p.stem for p in KILNS}


@pytest.mark.parametrize("path", KILNS, ids=lambda p: p.stem)
def test_a_built_kiln_builds_without_an_error(path: Path) -> None:
    kiln = load_design(path)
    assert type(kiln).model_validate(design_document(kiln)) == kiln
    report = design_report(kiln)
    assert [f.message for f in report.findings if f.level == "error"] == []
    warned = {_family(f.check.id) for f in report.findings if f.level == "warning" and f.check}
    assert warned == set(WARNED.get(path.stem, {}))


@pytest.mark.parametrize("path", KILNS, ids=lambda p: p.stem)
def test_each_kiln_cites_its_pages(path: Path) -> None:
    """Every design says where in the book it comes from, and what it had to assume."""
    head = path.read_text(encoding="utf-8").split("schema:")[0]
    assert "Olsen" in head
    assert "p." in head
