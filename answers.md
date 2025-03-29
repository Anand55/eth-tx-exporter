# 🧠 Bonus Questions – Ethereum Transaction Exporter

---

## 1️⃣ If you were designing this for a larger scale system, how would you structure & store the transaction data for easy retrieval?

### 🔨 Architecture for Scale

For a production-grade, large-scale system dealing with millions of transactions, I would implement the following:

**1. Ingestion Layer**
- Use **event-driven workers** or a **message queue** (e.g., Kafka/SQS) to decouple fetch, parse, and store processes
- Add support for scheduled re-syncs and failure retries

**2. Scalable Storage**
- **Raw storage** in a blob system (e.g., AWS S3 / GCS) for long-term archival
- **Structured storage** in a database:
  - Use **PostgreSQL** (or ClickHouse for high-performance analytics)
  - Normalize schema: `transactions`, `wallets`, `tokens`, etc.
  - Index on `address`, `timestamp`, `tx_hash`, and `block_number`

**3. Retrieval**
- RESTful API or GraphQL endpoint with filters: by address, token, time range, etc.
- Implement **caching** for commonly requested wallets

**4. Data Sync**
- Track sync state (e.g., last synced block per wallet) in a stateful store (e.g., Redis or DB)
- Support resume-on-failure and partial backfills

---

## 2️⃣ What trade-offs would you consider when handling more complex transactions beyond simple send/receive such as adding liquidity on Uniswap?

### 💡 Considerations for Complex DeFi Interactions

Handling DEX and DeFi interactions (like Uniswap, Compound, Aave) requires parsing **contract-level interactions**.

**Trade-offs:**

| Aspect | Simplified Parser | Advanced Decoder |
|--------|-------------------|------------------|
| ✅ Speed | Faster (skip inner calls) | Slower (parse logs + calldata) |
| 📦 Accuracy | Only captures top-level tx | Captures all sub-actions (e.g. LP tokens) |
| 🧠 Complexity | Easy to implement | Requires ABI decoding, event signature indexing |
| 🔍 Insight | Limited context (e.g., just "send") | Full semantic info (e.g., "add liquidity", "swap exact ETH") |

### 🛠️ Solution for DeFi Transactions

- Decode `input data` using contract ABI
- Use **log topics + indexed events** to detect:
  - `Swap`, `AddLiquidity`, `RemoveLiquidity`, etc.
- Classify transactions using known DEX routers and factories
- Maintain a **token registry** to correctly interpret LP tokens and routing behavior

---

✅ In short: for scale, I’d move to database-backed, event-driven ingestion. For complex DeFi txs, I’d invest in ABI parsing and event classification, possibly leveraging tools like **Dune**, **The Graph**, or **EVM traces**.

