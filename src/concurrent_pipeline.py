import os
import csv
import threading
from concurrent.futures import ThreadPoolExecutor
from fetcher import (
    fetch_normal_transactions,
    fetch_internal_transactions,
    fetch_erc20_transfers,
    fetch_erc721_transfers
)
from parser import (
    parse_normal_tx,
    parse_internal_tx,
    parse_erc20_tx,
    parse_erc721_tx
)

FIELDNAMES = [
    "hash", "timestamp", "from", "to", "type",
    "contract", "symbol", "token_id", "amount", "gas"
]

def pipeline_step(fetch_fn, parse_fn, address, csv_path, lock, label):
    """
    One complete pipeline: fetch → parse → write (thread-safe)
    """
    try:
        print(f"🔄 Starting pipeline for: {label}")
        parsed_txs = parse_fn(fetch_fn(address))
        rows = list(parsed_txs)

        with lock:
            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writerows(rows)

        print(f"✅ {label} done: Exported {len(rows)} transactions.\n")

    except Exception as e:
        print(f"❌ Error in {label}: {e}")


def run_concurrent_pipeline(address):
    print(f"\n🚀 Running fully concurrent pipeline for {address}\n")

    output_path = "data/output.csv"
    os.makedirs("data", exist_ok=True)

    # Create CSV and write header once
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()

    lock = threading.Lock()

    pipelines = [
        (fetch_normal_transactions, parse_normal_tx, "Normal ETH"),
        (fetch_internal_transactions, parse_internal_tx, "Internal"),
        (fetch_erc20_transfers, parse_erc20_tx, "ERC-20"),
        (fetch_erc721_transfers, parse_erc721_tx, "ERC-721"),
    ]

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(pipeline_step, fetch_fn, parse_fn, address, output_path, lock, label)
            for fetch_fn, parse_fn, label in pipelines
        ]
        for f in futures:
            f.result()  # block until all are done

    print("✅ All pipelines completed. Output: data/output.csv\n")
