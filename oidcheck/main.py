# oidcheck/main.py
import argparse
import json
import asyncio
from .validator import validate_config_async
from .models import AppConfig
from dotenv import dotenv_values


def main() -> None:
    parser = argparse.ArgumentParser(description="Flask OIDC Config Validator")
    parser.add_argument(
        "--file",
        "-f",
        default=".env",
        help="Path to configuration file (e.g., .env)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output validation results in JSON format",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with non-zero status on validation warnings",
    )
    args = parser.parse_args()

    config_values = dotenv_values(args.file)
    # Filter out None values and let Pydantic handle defaults
    filtered_values = {k: v for k, v in config_values.items() if v is not None}
    config = AppConfig(**filtered_values)  # type: ignore

    results = asyncio.run(validate_config_async(config))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(f"[{result['level']}] {result['message']}")

    if args.strict and any(r["level"] in ["WARNING", "ERROR"] for r in results):
        exit(1)


if __name__ == "__main__":
    main()
