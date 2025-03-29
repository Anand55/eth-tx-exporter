# Bonus Questions Answers

## 1. How would you scale this for 160,000+ transactions?

**a. Pagination + Batching:**
Use Etherscan's pagination to request data in manageable chunks. Automate batching logic with delays to respect rate limits.

**b. Rate-limiting resilience:**
Handle HTTP 429s gracefully. Implement retries with exponential backoff.

**c. Multithreading/Async (if allowed):**
Use async fetchers (e.g., with `httpx`) or threads to parallelize data retrieval without blocking.

**d. Chunked CSV writing:**
Instead of keeping all data in memory, write to CSV in chunks/streams.

**e. Extendable architecture:**
Support for job queue + background workers (e.g., Celery) if integrated into a web app later.

---

## 2. What are the tradeoffs of this approach for complex transactions?

**a. Etherscan API limitations:**
Doesn't capture all events or custom logic in DeFi smart contracts. Not reliable for deep decoding.

**b. Loss of context:**
Individual transfers might be part of larger multi-step DeFi transactions. This script treats each transfer atomically.

**c. No decoding of input data:**
We skip parsing `input` data from the transactions, so we can't infer exact contract actions like swaps, staking, etc.

**d. No ERC-1155 or contract execution logs:**
Those require log/event parsing or decoding via ABI, which this version skips for simplicity.

**e. One-way info:**
We rely on what Etherscan provides. For deeper insight, you'd need raw blockchain access (e.g., Alchemy trace API + ABIs).

