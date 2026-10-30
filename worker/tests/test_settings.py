from arq.worker import get_kwargs

from kilndesigner_api.settings import get_settings
from kilndesigner_worker.main import WorkerSettings


def test_the_worker_runs_as_many_builds_at_once_as_its_setting_says() -> None:
    # arq drops a WorkerSettings attribute it doesn't know, so check the name reaches it
    max_jobs: object = get_kwargs(dict(vars(WorkerSettings)))["max_jobs"]
    assert max_jobs == get_settings().worker_jobs
