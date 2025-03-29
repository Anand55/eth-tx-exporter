# ETH Transaction Exporter

This project extracts, parses, and exports Ethereum wallet transactions (ETH, ERC-20, ERC-721, internal) into a structured CSV file. Built for the CoinTracker hiring assignment.

---

## 🚀 Setup Instructions

1. **Clone the repo & enter directory**
```bash
cd eth-tx-exporter
```

2. **Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your Etherscan API key**
Create a `.env` file in the root:
```env
ETHERSCAN_API_KEY=your_key_here
```

5. **Run the script**
```bash
python src/main.py
```

Output CSV will be generated at `data/output.csv`

---

## 📁 Directory Structure

```
eth-tx-exporter/
├── src/
│   ├── main.py          # Entry point
│   ├── fetcher.py       # Fetch ETH, ERC-20, ERC-721, internal txns
│   ├── parser.py        # Normalize & standardize tx format
│   └── exporter.py      # Write to CSV
├── data/                # Output CSV lives here
├── .env                 # Etherscan API key
├── README.md            # This file
├── answers.md           # Bonus questions
└── requirements.txt     # Dependencies
```

---

## ✅ Assumptions
- Address is provided in code (can be adapted to CLI/args easily)
- Only inbound/outbound token transfers and ETH txs are considered
- Gas fee is calculated as `gasUsed * gasPrice` (in ETH)
- NFT transfers are assumed to be ERC-721 (ERC-1155 not handled in this version)

---

## 🧠 Design Choices
- **Modular**: Clear separation between fetch, parse, export
- **Scalable**: Easy to extend to CLI, web, batching, or other chains
- **Simple**: Zero external dependencies beyond `requests` and `dotenv`

---

## 📦 Output Fields
- Transaction Hash
- Date & Time (UTC)
- From Address
- To Address
- Transaction Type (ETH, ERC-20, ERC-721, INTERNAL)
- Asset Contract Address
- Symbol or Token Name
- Token ID (if NFT)
- Amount (ETH or Token units)
- Gas Fee (in ETH)

