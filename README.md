# Mini Search Engine

A small search engine built with Python, FastAPI, and PostgreSQL.

Features:
- Web crawler over local document corpus
- Inverted index with TF-IDF scoring
- PageRank ranking for query results
- PostgreSQL full-text search integration
- Caching, stemming, and stop-word filtering

## Run

1. Start PostgreSQL with Docker Compose:
   ```bash
   docker compose up -d
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```

## API

- `GET /search?q=<query>`
- `POST /documents` to add documents
