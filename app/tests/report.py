from pathlib import Path
import json
from decimal import Decimal
from enum import Enum


def json_serializer(obj):
    """
    Converts unsupported objects into JSON serializable values.
    """

    if isinstance(obj, Decimal):
        return float(obj)

    if isinstance(obj, Enum):
        return obj.value

    return str(obj)


def save_json(results, path):
    """
    Saves complete evaluation results as JSON.
    """

    with open(path, "w", encoding="utf-8") as f:

        json.dump(
            results,
            f,
            indent=4,
            ensure_ascii=False,
            default=json_serializer,
        )


def save_markdown(results, metrics, path):
    """
    Saves a human-readable evaluation report.
    """

    lines = []

    lines.append("# Supermarket AI Agent Evaluation Report\n")

    lines.append("## Summary\n")

    for key, value in metrics.items():
        lines.append(f"- **{key}** : {value}")

    lines.append("\n---\n")

    for index, result in enumerate(results, start=1):

        lines.append(f"## Test Case {index}\n")

        lines.append("### Query")

        lines.append("```")
        lines.append(result["query"])
        lines.append("```")

        lines.append(f"**Status:** {result['status']}")

        lines.append(f"**Latency:** {result['latency_ms']} ms")

        lines.append(f"**Retries:** {result['retry_count']}")

        lines.append(f"**Timestamp:** {result['timestamp']}")

        if result["error"]:

            lines.append("\n### Error")

            lines.append("```")
            lines.append(result["error"])
            lines.append("```")

        lines.append("\n### Response")

        lines.append("```")
        lines.append(str(result["response"]))
        lines.append("```")

        lines.append("\n---\n")

    Path(path).write_text(
        "\n".join(lines),
        encoding="utf-8",
    )