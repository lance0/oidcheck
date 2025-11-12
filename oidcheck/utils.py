# oidcheck/utils.py

"""
Utility functions for oidcheck.
"""

import json
from typing import List, Dict, Any, Optional


def format_validation_results(
    results: List[Dict[str, Any]], output_format: str = "text"
) -> str:
    """
    Format validation results for different output formats.

    Args:
        results: List of validation result dictionaries
        output_format: Output format ("text", "json", "html")

    Returns:
        Formatted string representation of results
    """
    if output_format == "json":
        return json.dumps(results, indent=2)
    elif output_format == "html":
        html_parts = []
        for result in results:
            level_class = f"result-{result['level'].lower()}"
            html_parts.append(
                f'<div class="{level_class}"><strong>{result["level"]}</strong>: '
                f"{result['message']}</div>"
            )
        return "\n".join(html_parts)
    else:  # text format
        return "\n".join(
            f"[{result['level']}] {result['message']}" for result in results
        )


def load_config_from_file(file_path: str) -> Dict[str, Optional[str]]:
    """
    Load configuration from various file formats.

    Currently supports .env files. Could be extended for YAML, TOML, etc.

    Args:
        file_path: Path to the configuration file

    Returns:
        Dictionary of configuration key-value pairs
    """
    from dotenv import dotenv_values

    return dotenv_values(file_path)
