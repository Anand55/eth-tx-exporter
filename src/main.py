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
from exporter import export_to_csv

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


    # Fetch raw transaction data
    normal_raw = fetch_normal_transactions(address)
    internal_raw = fetch_internal_transactions(address)
    erc20_raw = fetch_erc20_transfers(address)
    erc721_raw = fetch_erc721_transfers(address)

    # Parse into common structure
    print("🔍 Parsing transactions...")
    normal_parsed = parse_normal_tx(normal_raw)
    internal_parsed = parse_internal_tx(internal_raw)
    erc20_parsed = parse_erc20_tx(erc20_raw)
    erc721_parsed = parse_erc721_tx(erc721_raw)

    # Combine all
    all_tx = normal_parsed + internal_parsed + erc20_parsed + erc721_parsed

    # Export to CSV
    print("💾 Exporting {} transactions to CSV...\n".format(len(all_tx)))
    export_to_csv(all_tx)
    print("✅ Done! File saved at: data/output.csv\n")

if __name__ == "__main__":
    main()
