# src/exporter.py

import csv
import os

def export_to_csv(transactions, output_path="data/output.csv"):
    """Export parsed transactions to a CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    headers = [
        "Transaction Hash",
        "Date & Time",
        "From Address",
        "To Address",
        "Transaction Type",
        "Asset Contract Address",
        "Asset Symbol / Name",
        "Token ID",
        "Value / Amount",
        "Gas Fee (ETH)"
    ]

    with open(output_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for tx in transactions:
            writer.writerow({
                "Transaction Hash": tx.get("hash"),
                "Date & Time": tx.get("timestamp"),
                "From Address": tx.get("from"),
                "To Address": tx.get("to"),
                "Transaction Type": tx.get("type"),
                "Asset Contract Address": tx.get("contract"),
                "Asset Symbol / Name": tx.get("symbol"),
                "Token ID": tx.get("token_id"),
                "Value / Amount": tx.get("amount"),
                "Gas Fee (ETH)": tx.get("gas")
            })
