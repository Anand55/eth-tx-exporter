import argparse
from concurrent_pipeline import run_concurrent_pipeline

def main():
    parser = argparse.ArgumentParser(description="ETH Exporter - Fully Concurrent")
    parser.add_argument("--address", required=False)
    args = parser.parse_args()

    address = args.address or input("🔗 Enter Ethereum address: ").strip()
    run_concurrent_pipeline(address)

if __name__ == "__main__":
    main()
