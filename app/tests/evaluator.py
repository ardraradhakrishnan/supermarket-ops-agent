import asyncio
import random
import time
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv
from opentelemetry import metrics

from app.agents.agent_manager import AgentManager
from app.tests.queries import TEST_QUERIES
from app.tests.metrics import calculate_metrics
from app.tests.report import save_json, save_markdown

load_dotenv()


MAX_RETRIES = 5
RETRY_DELAY = 70      # seconds
MIN_DELAY = 15         # seconds between successful requests
MAX_DELAY = 20


async def ask_with_retry(manager, query):
    """
    Sends a query to the agent with automatic retry
    for Gemini rate limits.
    """

    retries = 0

    while True:

        try:
            response = await manager.chat(query)
            return response, retries, None

        except Exception as e:

            error = str(e)

            if (
                "RESOURCE_EXHAUSTED" in error
                or "429" in error
            ) and retries < MAX_RETRIES:

                retries += 1

                print(
                    f"Rate limit reached."
                    f" Waiting {RETRY_DELAY}s..."
                    f" Retry {retries}/{MAX_RETRIES}"
                )

                await asyncio.sleep(RETRY_DELAY)

                continue

            return None, retries, error


async def evaluate():

    manager = AgentManager()

    results = []

    total = len(TEST_QUERIES)

    for index, query in enumerate(TEST_QUERIES, start=1):

        print("=" * 80)
        print(f"[{index}/{total}] Running:")
        print(query)

        start = time.perf_counter()

        response, retries, error = await ask_with_retry(
            manager,
            query,
        )

        latency = round(
            (time.perf_counter() - start) * 1000,
            2,
        )

        results.append(
            {
                "query": query,
                "response": response,
                "status": "SUCCESS" if error is None else "FAILED",
                "error": error,
                "retry_count": retries,
                "latency_ms": latency,
                "tool_used": "Unknown",
                "timestamp": datetime.now().isoformat(),
            }
        )

        print(
            f"Completed in {latency:.2f} ms"
        )

        await asyncio.sleep(
            random.randint(
                MIN_DELAY,
                MAX_DELAY,
            )
        )

    metrics = calculate_metrics(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output = Path("app/tests/results")

    output.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_file = output / f"evaluation_{timestamp}.json"
    md_file = output / f"evaluation_{timestamp}.md"

    try:

        save_json(
            results,
            json_file,
        )

        print(f"\nJSON report saved:")
        print(json_file.resolve())

    except Exception as e:

        print("\nFailed to save JSON report")
        print(e)

    try:

        save_markdown(
            results,
            metrics,
            md_file,
        )

        print(f"\nMarkdown report saved:")
        print(md_file.resolve())

    except Exception as e:

        print("\nFailed to save Markdown report")
        print(e)

    print("\nEvaluation completed.\n")

    print(metrics)

if __name__ == "__main__":

    asyncio.run(evaluate())