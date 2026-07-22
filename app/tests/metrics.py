from collections import Counter


def calculate_metrics(results):
    """
    Calculates aggregate evaluation metrics.
    """

    total = len(results)

    successful = sum(
        1
        for r in results
        if r["status"] == "SUCCESS"
    )

    failed = total - successful

    average_latency = round(
        sum(r["latency_ms"] for r in results)
        / total,
        2,
    ) if total else 0

    retries = sum(
        r["retry_count"]
        for r in results
    )

    tool_usage = Counter(
        r["tool_used"]
        for r in results
    )

    success_rate = round(
        successful / total * 100,
        2,
    ) if total else 0

    return {
        "total_queries": total,
        "successful": successful,
        "failed": failed,
        "success_rate": f"{success_rate}%",
        "average_latency_ms": average_latency,
        "total_retries": retries,
        "tool_usage": dict(tool_usage),
    }