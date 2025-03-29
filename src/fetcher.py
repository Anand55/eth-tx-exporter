
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = "https://api.etherscan.io/api"

def fetch_normal_transactions(address):
    """Fetch external (normal) transactions for an ETH address."""
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_BASE_URL, params=params)
    data = response.json()
    return data.get("result", [])

def fetch_internal_transactions(address):
    """Fetch internal transactions (contract calls, etc.) for an ETH address."""
    params = {
        "module": "account",
        "action": "txlistinternal",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_BASE_URL, params=params)
    data = response.json()
    return data.get("result", [])

def fetch_erc20_transfers(address):
    """Fetch ERC-20 token transfers for an ETH address."""
    params = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_BASE_URL, params=params)
    data = response.json()
    return data.get("result", [])

def fetch_erc721_transfers(address):
    """Fetch ERC-721 (NFT) token transfers for an ETH address."""
    params = {
        "module": "account",
        "action": "tokennfttx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": ETHERSCAN_API_KEY
    }
    response = requests.get(ETHERSCAN_BASE_URL, params=params)
    data = response.json()
    return data.get("result", [])
