# -*- coding: utf-8 -*-
import argparse
import sys
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
from exporter import export_to_csv_streaming


def get_eth_address(cli_address):
    if cli_address:
        return cli_address.strip()

    address = input("🔗 Enter Ethereum address: ").strip()

    if not address:
        print("❌ Error: Ethereum address is required.")
        sys.exit(1)

    if not address.startswith("0x") or len(address) != 42:
        print("❌ Error: Invalid Ethereum address format.")
        sys.exit(1)

    return address


def main():
    parser = argparse.ArgumentParser(description="Ethereum Transaction Exporter")
    parser.add_argument("--address", help="Ethereum wallet address")
    args = parser.parse_args()

    address = get_eth_address(args.address)
    print("\n📥 Fetching transactions for: {}\n".format(address))
    print("🔍 Parsing and exporting transactions...\n")

    # Stream parsed transactions directly to CSV with buffered writes
    export_to_csv_streaming([
        parse_normal_tx(fetch_normal_transactions(address)),
        parse_internal_tx(fetch_internal_transactions(address)),
        parse_erc20_tx(fetch_erc20_transfers(address)),
        parse_erc721_tx(fetch_erc721_transfers(address)),
    ])

    print("✅ Done! File saved at: data/output.csv\n")


if __name__ == "__main__":
    main()
