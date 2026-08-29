import json
import re
from typing import Any, Dict


def sanitize_json_response(response: str) -> Dict[str, Any]:
    """Extract JSON from a model response and return a dict."""
    if not response:
        return {}

    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("` ")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return {}

    return {}
