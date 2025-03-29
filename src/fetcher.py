# -*- coding: utf-8 -*-
import os
import requests
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()

ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
BASE_URL = "https://api.etherscan.io/api"


def fetch_paginated_data(address, action, offset=1000, max_pages=20, workers=5):
    """
    Generic concurrent paginated fetcher using page + offset.
    Supports ETH, ERC-20, ERC-721, and internal transactions.
    """

    def fetch_page(page):
        params = {
            "module": "account",
            "action": action,
            "address": address,
            "page": page,
            "offset": offset,
            "sort": "asc",
            "apikey": ETHERSCAN_API_KEY
        }
        try:
            print(f"⚙️ Fetching {action} page {page}...")
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            if data["status"] == "1" and data["result"]:
                return data["result"]
            else:
                return []
        except Exception as e:
            print(f"❌ Error on page {page} ({action}): {e}")
            return []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(fetch_page, page) for page in range(1, max_pages + 1)]

        for future in as_completed(futures):
            transactions = future.result()
            for tx in transactions:
                yield tx


# Public wrappers for each type
def fetch_normal_transactions(address, offset=1000, max_pages=20, workers=5):
    return fetch_paginated_data(address, action="txlist", offset=offset, max_pages=max_pages, workers=workers)


def fetch_internal_transactions(address, offset=1000, max_pages=20, workers=5):
    return fetch_paginated_data(address, action="txlistinternal", offset=offset, max_pages=max_pages, workers=workers)


def fetch_erc20_transfers(address, offset=1000, max_pages=20, workers=5):
    return fetch_paginated_data(address, action="tokentx", offset=offset, max_pages=max_pages, workers=workers)


def fetch_erc721_transfers(address, offset=1000, max_pages=20, workers=5):
    return fetch_paginated_data(address, action="tokennfttx", offset=offset, max_pages=max_pages, workers=workers)
