"""
Ultimate Brain — Multi-Worker Execution Engine
Parallel processing of large stock universes for institutional-grade speed.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed


def run_parallel(symbols, worker_function, max_workers=8):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker_function, s): s for s in symbols}

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception:
                pass

    return results
