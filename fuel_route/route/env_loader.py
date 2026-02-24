"""
Load variables from .env file only (no Django settings).
.env is read from project root (parent of directory containing manage.py).
"""
from pathlib import Path


def _env_path() -> Path:
    # route/env_loader.py -> route/ -> fuel_route (inner) -> project root
    return Path(__file__).resolve().parent.parent.parent / ".env"


def load_env() -> dict:
    """Return dict of KEY=value from .env file. Keys/values stripped."""
    path = _env_path()
    out = {}
    if not path.exists():
        return out
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                out[key.strip()] = value.strip()
    return out


def get_openroute_api_key() -> str:
    return load_env().get("OPENROUTESERVICE_API_KEY", "").strip()
