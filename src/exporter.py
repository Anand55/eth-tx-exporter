import csv
import os

def export_to_csv_streaming(generator_list, output_path="data/output.csv", buffer_size=500):
    """
    Streams transactions to CSV using buffered batch writes.
    """
    os.makedirs("data", exist_ok=True)

    fieldnames = [
        "hash", "timestamp", "from", "to", "type",
        "contract", "symbol", "token_id", "amount", "gas"
    ]

    tx_count = 0
    buffer = []

    with open(output_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for generator in generator_list:
            for tx in generator:
                buffer.append(tx)
                tx_count += 1

                if len(buffer) >= buffer_size:
                    writer.writerows(buffer)
                    buffer.clear()

        # Write any remaining txs
        if buffer:
            writer.writerows(buffer)

    if tx_count == 0:
        print("⚠️ No transactions found for this wallet.")
    else:
        print("✅ Exported {} transactions.".format(tx_count))
