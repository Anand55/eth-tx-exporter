# 🚀 Ethereum Transaction Exporter

A fast, concurrent Python-based tool to export Ethereum wallet transactions to a CSV file — supports:

- ✅ Normal ETH transactions  
- ✅ Internal transactions  
- ✅ ERC-20 token transfers  
- ✅ ERC-721 (NFT) transfers

Built with concurrency, batching, and reliability in mind. Works with the free Etherscan API tier.

---

## ⚙️ Architecture Overview

The tool uses a multi-threaded pipeline:

1. **4 Threads** run in parallel — one for each transaction type (ETH, Internal, ERC-20, ERC-721)
2. Each thread:
   - Fetches paginated data from Etherscan using `page` + `offset`
   - Parses it into a unified format
   - Batches results (1000 per batch) and writes to a shared CSV
3. Thread-safe writing is ensured using `threading.Lock`
4. The total number of exported transactions is tracked and displayed

All logic lives inside `src/concurrent_pipeline.py`.

---

## 📦 Example: Export from a Real Address

Let’s test this with a known active address:  
`0xfb50526f49894b78541b776f5aaefe43e3bd8590`

### Run Locally:

```bash
python -m src.main --address 0xfb50526f49894b78541b776f5aaefe43e3bd8590
```

### Output:

```
✅ Normal ETH done: Exported 53 transactions.
✅ ERC-20 done: Exported 8341 transactions.
✅ Internal done: Exported 0 transactions.
✅ ERC-721 done: Exported 0 transactions.
🔢 Total transactions exported: 8394
✅ All pipelines completed. Output: data/output.csv
```

---

## 🐍 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/eth-tx-exporter.git
cd eth-tx-exporter
```

### 2. Create a `.env` file

```
ETHERSCAN_API_KEY=your_etherscan_key_here
```

Get a free API key: [etherscan.io/apis](https://etherscan.io/apis)

### 3. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the exporter

```bash
python -m src.main --address 0xfb50526f49894b78541b776f5aaefe43e3bd8590
```

---

## 🐳 Run with Docker

### 1. Build the Docker image

```bash
docker build -t eth-tx-exporter .
```

### 2. Run with environment variable

```bash
docker run --rm   -e ETHERSCAN_API_KEY=your_etherscan_key_here   eth-tx-exporter --address 0xfb50526f49894b78541b776f5aaefe43e3bd8590
```

### 3. Mount local volume to access CSV output:

```bash
docker run --rm   -v $(pwd)/data:/app/data   -e ETHERSCAN_API_KEY=your_etherscan_key_here   eth-tx-exporter --address 0xfb50526f49894b78541b776f5aaefe43e3bd8590
```

Output file: `./data/output.csv`

---

## 🧪 Run Unit Tests

Includes tests for:
- ✅ Transaction parsing logic
- ✅ Thread-safe CSV writing

### Run all tests:

```bash
python3 -m unittest discover tests
```

---

## ✅ Features

- 🧵 Threaded pipeline (1 per tx type)
- 🧾 Batching of 1000 transactions per write
- 🔐 Thread-safe CSV export with locks
- 🔁 Reliable pagination with page + offset
- 🆓 Works with free Etherscan API
- 🐳 Docker support for zero-setup runs

---

## 📁 Output

Exports all transactions to a single CSV file:

```
data/output.csv
```

With fields like:

```
hash,timestamp,from,to,type,contract,symbol,token_id,amount,gas
```

---

## 💡 Future Ideas

- ✅ Add resume support via last block checkpoint
- ✅ Optional filtering by block range or time
- ✅ Split exports by tx type
- ✅ Postgres export option

---

