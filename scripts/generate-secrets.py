"""Generate local FireGuard secrets without overwriting real values."""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import secrets
from pathlib import Path

PLACEHOLDER_MARKERS = (
    "replace-",
    "replace_",
    "your-",
    "your_",
    "changeme",
    "<sha256",
    "<",
)


def is_placeholder(value: str) -> bool:
    normalized = value.strip().strip('"').strip("'")
    return not normalized or any(marker in normalized.lower() for marker in PLACEHOLDER_MARKERS)


def read_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.lstrip().startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def set_env(path: Path, updates: dict[str, str]) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    changed: list[str] = []
    seen: set[str] = set()
    output: list[str] = []
    for line in lines:
        if "=" not in line or line.lstrip().startswith("#"):
            output.append(line)
            continue
        key = line.split("=", 1)[0].strip()
        if key in updates:
            output.append(f"{key}={updates[key]}")
            seen.add(key)
            changed.append(key)
        else:
            output.append(line)
    for key, value in updates.items():
        if key not in seen:
            output.append(f"{key}={value}")
            changed.append(key)
    path.write_text("\n".join(output) + "\n", encoding="utf-8")
    return changed


def generated_or_existing(values: dict[str, str], key: str, factory) -> str:
    value = values.get(key, "")
    return value if value and not is_placeholder(value) else factory()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()

    api_env = root / "fireguard-api" / ".env"
    intake_env = root / "fireguard-agent-intake" / ".env"
    report_env = root / "fireguard-agent-report" / ".env"
    for path in (api_env, intake_env, report_env):
        if not path.exists():
            print(f"SKIP {path}: run 'task setup-env' first")

    api_values = read_env(api_env)
    intake_values = read_env(intake_env)
    report_values = read_env(report_env)

    postgres_password = generated_or_existing(
        api_values, "POSTGRES_PASSWORD", lambda: secrets.token_urlsafe(24)
    )
    internal_api_key = generated_or_existing(
        api_values, "INTERNAL_API_KEY", lambda: f"fg_{secrets.token_urlsafe(32)}"
    )
    jwt_secret = generated_or_existing(
        api_values, "JWT_SECRET", lambda: secrets.token_urlsafe(32)
    )
    signing_secret = generated_or_existing(
        report_values, "SIGNING_SECRET", lambda: secrets.token_urlsafe(32)
    )
    upload_key = generated_or_existing(
        intake_values,
        "UPLOAD_ENCRYPTION_KEY",
        lambda: base64.urlsafe_b64encode(os.urandom(32)).decode("ascii"),
    )
    api_key_hash = hashlib.sha256(internal_api_key.encode("utf-8")).hexdigest()
    report_api_keys = report_values.get("API_KEYS", "")
    if not report_api_keys or is_placeholder(report_api_keys) or report_api_keys == "[]":
        report_api_keys = f'["gateway:{api_key_hash}"]'

    if api_env.exists():
        changed = set_env(
            api_env,
            {
                "POSTGRES_PASSWORD": postgres_password,
                "DATABASE_URL": f"postgresql://fireguard:{postgres_password}@postgres:5432/fireguard",
                "JWT_SECRET": jwt_secret,
                "INTERNAL_API_KEY": internal_api_key,
            },
        )
        print(f"UPDATED fireguard-api/.env: {', '.join(changed) or 'none'}")
    if intake_env.exists():
        changed = set_env(intake_env, {"UPLOAD_ENCRYPTION_KEY": upload_key})
        print(f"UPDATED fireguard-agent-intake/.env: {', '.join(changed) or 'none'}")
    if report_env.exists():
        changed = set_env(
            report_env,
            {
                "SIGNING_SECRET": signing_secret,
                "API_KEYS": report_api_keys,
            },
        )
        print(f"UPDATED fireguard-agent-report/.env: {', '.join(changed) or 'none'}")

    print("Generated or preserved local secrets successfully.")
    print("MANUAL: set GROQ_API_KEY and GEMINI_API_KEY in the services that use them.")


if __name__ == "__main__":
    main()
