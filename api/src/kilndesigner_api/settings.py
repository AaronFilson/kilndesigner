"""Settings, read from ``KILNDESIGNER_*`` environment variables."""

from __future__ import annotations

from functools import cache
from pathlib import Path

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="KILNDESIGNER_", env_file=".env", extra="ignore")

    # 127.0.0.1 rather than localhost: on Windows, localhost tries IPv6 first, and the compose
    # file publishes its ports on IPv4 only
    database_url: str = "postgresql+asyncpg://kilndesigner:kilndesigner@127.0.0.1:5432/kilndesigner"
    redis_url: str = "redis://127.0.0.1:6379/0"
    data_dir: Path = Path("data")
    """Where built files go: ``<data_dir>/builds/<build key>/``."""
    jobs: str = "arq"
    """``arq`` sends builds to the worker; ``inline`` runs them in the API process."""
    worker_jobs: PositiveInt = 10
    """How many builds the worker runs at once (10 is arq's default). Each one wants a CPU and a
    few hundred MB, so a small machine should run one at a time."""
    cors_origins: list[str] = ["http://localhost:5173"]


@cache
def get_settings() -> Settings:
    return Settings()
