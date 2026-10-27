"""Backend configuration. Never serialize settings into logs or API responses."""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    anthropic_api_key: str = field(default="", repr=False)
    anthropic_model: str = ""
    supabase_url: str = ""
    supabase_secret_key: str = field(default="", repr=False)
    aws_region: str = "us-east-1"


def load_settings(env_file: str | Path = ".env") -> Settings:
    """Load local values while letting deployed environment variables take precedence."""
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=env_file, override=False)
    return Settings(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
        anthropic_model=os.getenv("ANTHROPIC_MODEL", ""),
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_secret_key=os.getenv("SUPABASE_SECRET_KEY", ""),
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
    )
