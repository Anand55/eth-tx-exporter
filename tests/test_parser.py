import unittest
from src.parser import parse_normal_tx, parse_erc20_tx

class TestParser(unittest.TestCase):

    def test_parse_normal_tx(self):
        raw = [{
            "hash": "0x123",
            "timeStamp": "1700000000",
            "from": "0xaaa",
            "to": "0xbbb",
            "value": "1000000000000000000",
            "gasPrice": "1000000000",
            "gasUsed": "21000"
        }]
        parsed = parse_normal_tx(raw)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["hash"], "0x123")
        self.assertEqual(parsed[0]["type"], "ETH")
        self.assertEqual(parsed[0]["amount"], 1.0)

    def test_parse_erc20_tx(self):
        raw = [{
            "hash": "0x456",
            "timeStamp": "1700000001",
            "from": "0xccc",
            "to": "0xddd",
            "value": "2500000",
            "contractAddress": "0xtoken",
            "tokenSymbol": "USDT",
            "gasPrice": "1000000000",
            "gasUsed": "60000"
        }]
        parsed = parse_erc20_tx(raw)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["symbol"], "USDT")
        self.assertAlmostEqual(parsed[0]["amount"], 2.5e-12)

if __name__ == "__main__":
    unittest.main()
