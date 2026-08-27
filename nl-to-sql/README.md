# NL-to-SQL — Intent-Aware Data Assistant

A production-oriented Natural Language to SQL application built with **Python, Claude, SQLite and Streamlit**.

Ask questions about a local database in plain English. The application first classifies the user's intent, routes data questions to schema-aware SQL generation, validates the generated SQL, and executes only safe read-only queries. Non-data questions are handled conversationally instead of being forced into SQL.

## Architecture

```text
User Question
     |
     v
Intent Classification (Claude)
     |
     +---- DATA_QUERY ----> Schema Context -> SQL Generation -> SQL Validation -> SQLite
     |
     +---- NON_DATA_QUERY -> Conversational Response
     |
     +---- UNSAFE/UNKNOWN -> Safe Fallback
```

## V1 Features

- Claude API for intent classification and response generation
- Intent-aware routing: `DATA_QUERY`, `NON_DATA_QUERY`, `UNSAFE_QUERY`, `UNKNOWN`
- Automatic SQLite schema discovery
- Natural language to SQL generation
- Read-only SQL validation with SQLGlot
- Table/column validation against the live schema
- Bounded SQL regeneration when validation fails
- Streamlit UI
- Sample e-commerce database and seed data
- Unit tests without requiring a live LLM
- Docker support
- GitHub Actions CI

## Example questions

- `How many customers do we have?`
- `Which are the top 10 products by revenue?`
- `What was monthly revenue in 2025?`
- `Which customers placed the most orders?`
- `What is a data warehouse?` → handled as a non-data question, not SQL

## Quick start

```bash
cd nl-to-sql
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add ANTHROPIC_API_KEY to .env
python scripts/init_db.py
streamlit run app.py
```

## Configuration

```text
ANTHROPIC_API_KEY=your-key
ANTHROPIC_MODEL=claude-haiku-4-5-20251001
MAX_SQL_RETRIES=2
```

## Project structure

```text
nl-to-sql/
├── app.py
├── src/
│   ├── config.py
│   ├── database.py
│   ├── schema_inspector.py
│   ├── llm_client.py
│   ├── prompt_builder.py
│   ├── sql_generator.py
│   ├── sql_validator.py
│   ├── sql_executor.py
│   └── orchestrator.py
├── prompts/
│   ├── intent_classification.txt
│   ├── sql_generation.txt
│   └── non_data_response.txt
├── data/
│   └── seed.sql
├── scripts/
│   └── init_db.py
├── tests/
│   ├── test_schema_inspector.py
│   ├── test_sql_validator.py
│   └── test_orchestrator.py
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Safety model

The LLM is never trusted as the final authority. Generated SQL passes through deterministic validation before execution. V1 permits only read-only `SELECT` queries and rejects destructive statements such as `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER` and `CREATE`.

## Roadmap

- [x] Intent classification
- [x] Schema-aware SQL generation
- [x] Read-only SQL validation
- [x] Error recovery and bounded retry
- [x] Streamlit UI
- [x] Tests and CI
- [ ] Semantic metrics and business definitions
- [ ] RAG-based schema retrieval
- [ ] PostgreSQL support
- [ ] Query explanation and visualisation
- [ ] Evaluation dataset and LLM-as-judge metrics

## Author

**Lakshmi Priyanka Kaduluri** — Data Engineering | AWS | Databricks | AI Engineering
