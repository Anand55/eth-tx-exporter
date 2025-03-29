
from datetime import datetime

def parse_normal_tx(tx_list):
    """Parse normal ETH transfers."""
    parsed = []
    for tx in tx_list:
        parsed.append({
            "hash": tx.get("hash"),
            "timestamp": convert_timestamp(tx.get("timeStamp")),
            "from": tx.get("from"),
            "to": tx.get("to"),
            "type": "ETH",
            "contract": None,
            "symbol": "ETH",
            "token_id": None,
            "amount": int(tx.get("value", 0)) / 1e18,
            "gas": int(tx.get("gasUsed", 0)) * int(tx.get("gasPrice", 0)) / 1e18 if tx.get("gasUsed") else None
        })
    return parsed

def parse_internal_tx(tx_list):
    """Parse internal contract-triggered transfers."""
    parsed = []
    for tx in tx_list:
        parsed.append({
            "hash": tx.get("hash"),
            "timestamp": convert_timestamp(tx.get("timeStamp")),
            "from": tx.get("from"),
            "to": tx.get("to"),
            "type": "INTERNAL",
            "contract": None,
            "symbol": "ETH",
            "token_id": None,
            "amount": int(tx.get("value", 0)) / 1e18,
            "gas": None
        })
    return parsed

def parse_erc20_tx(tx_list):
    """Parse ERC-20 token transfers."""
    parsed = []
    for tx in tx_list:
        parsed.append({
            "hash": tx.get("hash"),
            "timestamp": convert_timestamp(tx.get("timeStamp")),
            "from": tx.get("from"),
            "to": tx.get("to"),
            "type": "ERC-20",
            "contract": tx.get("contractAddress"),
            "symbol": tx.get("tokenSymbol"),
            "token_id": None,
            "amount": int(tx.get("value", 0)) / (10 ** int(tx.get("tokenDecimal", 18))),
            "gas": int(tx.get("gasUsed", 0)) * int(tx.get("gasPrice", 0)) / 1e18 if tx.get("gasUsed") else None
        })
    return parsed

def parse_erc721_tx(tx_list):
    """Parse ERC-721 (NFT) transfers."""
    parsed = []
    for tx in tx_list:
        parsed.append({
            "hash": tx.get("hash"),
            "timestamp": convert_timestamp(tx.get("timeStamp")),
            "from": tx.get("from"),
            "to": tx.get("to"),
            "type": "ERC-721",
            "contract": tx.get("contractAddress"),
            "symbol": tx.get("tokenSymbol"),
            "token_id": tx.get("tokenID"),
            "amount": 1,  # Always 1 for NFT transfers
            "gas": int(tx.get("gasUsed", 0)) * int(tx.get("gasPrice", 0)) / 1e18 if tx.get("gasUsed") else None
        })
    return parsed

def convert_timestamp(ts):
    """Convert UNIX timestamp to ISO format."""
    return datetime.utcfromtimestamp(int(ts)).isoformat() if ts else None
