# oidcheck/main.py
import argparse
import json
from .validator import validate_config
from .models import AppConfig
from dotenv import dotenv_values

def main():
    parser = argparse.ArgumentParser(description="Flask OIDC Config Validator")
    parser.add_argument("--file", "-f", default=".env", help="Path to the configuration file (e.g., .env)")
    parser.add_argument("--json", action="store_true", help="Output validation results in JSON format")
    parser.add_argument("--strict", action="store_true", help="Exit with a non-zero status code on validation warnings")
    args = parser.parse_args()

    config_values = dotenv_values(args.file)
    config = AppConfig(**config_values)

    results = validate_config(config)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            print(f"[{result['level']}] {result['message']}")

    if args.strict and any(r['level'] in ['WARNING', 'ERROR'] for r in results):
        exit(1)

if __name__ == "__main__":
    main()
