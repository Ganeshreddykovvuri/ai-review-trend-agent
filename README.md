# AI Review Trend Analysis Agent (Swiggy – Google Play Store)

## 📌 Overview

This project implements an **Agentic AI system** to analyze **daily Google Play Store reviews** for the Swiggy food delivery app and generate a **30-day rolling trend analysis** of user issues, complaints, and feature requests.

Each day’s reviews are treated as a **batch**, processed by AI agents, and aggregated into a **topic × date frequency table** that helps product teams identify:
- Recurring problems
- Emerging issues
- Feature requests gaining traction
- Gaps in app or service experience

---

## 🎯 Problem Statement

Given:
- An app store link (Swiggy)
- A target date **T**

Design a system that:
1. Consumes **daily review batches** starting from June 1, 2024
2. Extracts **issues, requests, and feedback**
3. Consolidates **similar but non-identical topics**
4. Produces a **trend report from T-30 to T**

### Output Requirements
- **Rows:** Topics (issues / requests)
- **Columns:** Dates from T-30 → T
- **Cells:** Frequency of topic occurrence on that date

Days with no reviews must appear with **0** counts (no data fabrication).

---

## 🧠 Why Agentic AI (Not LDA / BERTopic)

Traditional topic modeling:
- Struggles with short, noisy app reviews
- Produces fragmented or unstable topics
- Has low recall for edge cases

This system uses **Agentic AI** with LLMs to:
- Extract high-recall, actionable topics
- Reason across paraphrases
- Deduplicate semantically similar issues
- Adapt to new, evolving problems

---

## 🏗️ System Architecture

Google Play Store Reviews

↓

Daily Ingestion (JSON)

↓

Understanding Agent (LLM)

↓

Canonicalization Agent (Deduplication)

↓

Aggregation Agent (Time Series)

↓

CSV Trend Report


---

## 🤖 Agents Description

### 1️⃣ Review Ingestion Agent
- Reads reviews from `reviews_raw.json`
- Groups reviews by date
- Treats each date as an independent batch

---

### 2️⃣ Review Understanding Agent
- Uses an LLM (via OpenRouter)
- Extracts **specific, Swiggy-focused issues**
- Avoids generic labels

Example topics:
- Delivery delay
- Delivery partner rude
- Food quality – cold / stale
- Instamart night availability
- Bolt (10-minute) delivery removed
- App crashes
- GPS / address issues
- Payment / refund problems

---

### 3️⃣ Topic Canonicalization Agent
- Prevents duplicate or fragmented topics
- Merges paraphrases into a **single canonical topic**
- Maintains long-term memory in `topic_store.json`
- Includes defensive validation to block verbose LLM responses

Example:
“delivery guy was impolite”
“delivery partner behaved badly”
→ Delivery Partner Rude


---

### 4️⃣ Aggregation Agent
- Builds a **topic × date frequency matrix**
- Ensures **all dates from T-30 → T exist**
- Missing days are filled with `0`

---

### 5️⃣ Report Agent
- Writes the final trend table to CSV
- Safely creates output directories
- Overwrites files without permission issues

---

## 📊 Output Format

Example CSV:

| Topic | 2025-06-01 | 2025-06-02 | … | 2025-06-30 |
|-----|-----------|-----------|---|-----------|
| Delivery Delay | 1 | 0 | … | 0 |
| Food Quality – Stale | 0 | 1 | … | 0 |
| Bolt Delivery Removed | 0 | 0 | … | 1 |

---

---

## 🔄 Data Source (Google Play Store)

Swiggy does not expose a public review API.

This system uses **Google Play Store reviews**, which are:
- Publicly accessible
- Collected daily
- Stored locally as JSON

The pipeline supports real-time ingestion by appending new reviews daily.

---

## ⚙️ How to Run

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt


setx OPENAI_API_KEY "sk-or-v1-xxxxxxxxxxxxxxxx"

Restart terminal after running this.

The key is never stored in code or GitHub.

python main.py

# OUTPUT IS STORED AS

output/trend_report_<TARGET_DATE>.csv




