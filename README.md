AI Review Agent
================

Purpose
-------
This repository provides a lightweight pipeline for ingesting, canonicalizing, analyzing, and reporting on app reviews using multiple small agent modules. It's intended as a starting point for automated review analysis and trend reporting.

Project structure
-----------------
- `main.py` — runner that orchestrates the pipeline.
- `requirements.txt` — Python dependencies.
- `agents/` — agent modules used by the pipeline:
  - `ingestion_agent.py` — loads raw review data.
  - `canonicalization_agent.py` — normalizes and cleans review text.
  - `understanding_agent.py` — extracts topics/sentiment from reviews.
  - `aggregation_agent.py` — aggregates analysis results.
  - `report_agent.py` — formats and writes report outputs.
  - `openrouter_client.py` — optional client for LLM service calls.
- `data/reviews_raw.json` — source reviews (input).
- `memory/topic_store.json` — persisted topic store used by agents.
- `output/` — generated reports (CSV files).
- `scripts/fetch_playstore_reviews.py` — helper to fetch reviews externally.

Quickstart
----------
1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the pipeline:

   ```bash
   python main.py
   ```

Notes
-----
- Input: place or update raw review data in `data/reviews_raw.json` before running.
- Outputs: generated CSV reports are stored in `output/` (example: `trend_report_2025-06-30.csv`).
- To fetch Play Store reviews automatically, see `scripts/fetch_playstore_reviews.py`.
- If using an LLM service, configure credentials for `openrouter_client.py` or adapt the client.

Recommended next steps
----------------------
- Add a small `README` section for each agent describing inputs/outputs.
- Add a sample `data/reviews_raw.json` snippet or test fixtures.
- Add a CI job or a script to regenerate reports automatically.

License & Contact
-----------------
This project has no license file by default. Add a `LICENSE` if you plan to share.
For questions or help, open an issue or contact the repository owner.
