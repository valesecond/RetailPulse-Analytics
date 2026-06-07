# RetailPulse Analytics

A modern, elegant analytics toolkit for retail sales — ready to run locally with Docker.

Key features

- Dataset translation to Portuguese (pt-BR) while keeping the original English dataset.
- Lightweight ETL with `pandas` and load into PostgreSQL (`retailpulse`).
- Portuguese SQL views for ready-to-use queries and dashboards.
- Metabase automation: create cards, embed dashboard images, and position tiles via Playwright.

Badges

- Local Docker · Metabase · PostgreSQL · Python

Prerequisites

- Docker & Docker Compose
- Python 3.10+ (for auxiliary scripts)

Quick Start

1. Start services:

```powershell
docker compose up -d
```

2. Open Metabase: visit `http://localhost:3000` and finish the onboarding.

3. (Optional) Run the pipeline to generate CSVs and load the database:

```powershell
python main.py
```

Repository structure (high level)

- `docker-compose.yml` — Postgres, Metabase, and supporting services
- `main.py` — pipeline entrypoint
- `src/` — ETL helpers: `extract.py`, `transform.py`, `load.py`
- `data/` — `raw/` and `processed/` (`clean_sales.csv`, `clean_sales_pt_br.csv`)
- `sql/` — views and SQL scripts (`views.sql`, `queries.sql`)
- `metabase/` — automation scripts and utilities for Metabase
- `dashboard/` — exported dashboards and SVG assets

ETL & Database notes

- The pipeline reads `data/raw/sales.csv`, produces cleaned outputs in `data/processed/` and loads them into Postgres tables.
- To keep dependent views stable, database loading uses `DELETE` + `INSERT` instead of a table `REPLACE`.
- Default DB connection when running via `docker-compose`: host `postgres`, db `retailpulse`, user/password `postgres`.

Metabase automation

- Useful scripts in `metabase/`:
  - `create_kpis_and_top10.py` — create KPI and top-10 cards
  - `embed_images_in_dashboard_metadata.py` — embed SVGs into dashboard JSON
  - `push_dashboard_metadata.py` — push updated dashboard metadata to Metabase
  - `create_image_markdown_cards.py` — create markdown cards that show embedded images
  - `playwright_add_cards.py` / `playwright_position_tiles.py` — UI automation to add and place cards (run locally in headed mode)

Environment variables for Metabase scripts
Set these before running scripts that call the Metabase API:

```powershell
$env:METABASE_USER='your_email'
$env:METABASE_PASS='your_password'
$env:METABASE_URL='http://localhost:3000'
python metabase\create_image_markdown_cards.py
```

Extract embedded SVGs

- The dashboard JSON with embedded images is `dashboard/dashboard_4_with_images.json`.
  To extract the embedded files into `dashboard/` run:

```powershell
python metabase\extract_embedded_svgs.py
```

Automatic tile positioning (Playwright)

- `metabase/playwright_position_tiles.py` reads `metabase/dashboard_layout.json` with percent coordinates and drags tiles into place.
- Run headed locally for best results.

```powershell
pip install playwright
python -m playwright install
$env:METABASE_USER='your_email'
$env:METABASE_PASS='your_password'
python metabase\playwright_position_tiles.py
```

Troubleshooting

- If a card fails to render, run `metabase/verify_cards.py` to inspect failing queries.
- If the API returns 404 for attaching cards, use the Playwright fallback scripts to add cards through the UI.

Contributing

- PRs welcome — improvements to SQL views, dashboard layout, or automation scripts are great.

License

- (Add a license if you want to open-source this project)

Contact

- Open an issue or attach screenshots if you need help.

Thank you for using RetailPulse — turn data into decisions.

## Project focus: Data, Notebooks, SQL and `src`

This project prioritizes the data pipeline, exploratory notebooks, SQL artifacts and the ETL source code. If you only need to understand or modify the core analytics components, read the sections below.

- Data:
  - Raw data lives in `data/raw/` and cleaned outputs are in `data/processed/`.
  - Main files: `data/raw/sales.csv`, `data/processed/clean_sales.csv`, `data/processed/clean_sales_pt_br.csv`.

- Notebooks (`notebooks/`):
  - `01_data_exploration.ipynb` — initial profiling, missing values, types, and column overview.
  - `02_sales_visual_analysis.ipynb` — charts and visual analysis for trends and seasonality.
  - `03_business_insights.ipynb` — KPI calculations and business-focused summaries.

- SQL (`sql/`):
  - `schema.sql` — table definitions (if used).
  - `queries.sql` — reusable SQL snippets.
  - `views.sql` — production-ready views (English and Portuguese versions) designed to simplify dashboard queries.

- Source (ETL) — `src/`:
  - `extract.py` — read and normalize source CSVs.
  - `transform.py` — cleaning, type casting and `translate_to_pt_br(df)` for Portuguese translation.
  - `load.py` — insert/update logic for PostgreSQL using `DELETE` + `INSERT` to preserve dependent views.

Best practices

- Start with `notebooks/01_data_exploration.ipynb` when changing the pipeline to understand impact.
- Keep SQL parameter-free where possible to avoid syntax incompatibilities with Postgres.
- Add small notebooks for manual checks when modifying `transform.py`.

If you want, I can now:

- add a `docs/data_dictionary.md` generated from `data/processed/clean_sales.csv`, or
- add unit tests for `src/transform.py` to validate transformations.
