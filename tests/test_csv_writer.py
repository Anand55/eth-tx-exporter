import unittest
import os
import csv
from threading import Lock
from src.concurrent_pipeline import FIELDNAMES

class TestCSVWriter(unittest.TestCase):
    def setUp(self):
        self.output_path = "tests/test_concurrent_output.csv"
        self.lock = Lock()
        self.sample_data = [
            {
                "hash": "0xtx1",
                "timestamp": "2025-03-29T12:00:00",
                "from": "0xabc",
                "to": "0xdef",
                "type": "ETH",
                "contract": None,
                "symbol": "ETH",
                "token_id": None,
                "amount": 0.42,
                "gas": 0.00021
            },
            {
                "hash": "0xtx2",
                "timestamp": "2025-03-29T12:01:00",
                "from": "0x123",
                "to": "0x456",
                "type": "ERC-20",
                "contract": "0xtoken",
                "symbol": "USDT",
                "token_id": None,
                "amount": 50.0,
                "gas": 0.00031
            }
        ]

    def test_batch_csv_write(self):
        # Write header
        with open(self.output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

        # Simulate writer in thread
        with self.lock:
            with open(self.output_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                writer.writerows(self.sample_data)

        # Read and validate
        with open(self.output_path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["hash"], "0xtx1")
            self.assertEqual(rows[1]["type"], "ERC-20")

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)

if __name__ == "__main__":
    unittest.main()
