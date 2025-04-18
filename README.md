# 📊 Financial Data ETL & Dashboard

This project provides an end-to-end ETL pipeline and interactive dashboard for financial stock data using the `yfinance` API. 
It loads, transforms, and stores historical market data in a PostgreSQL database, and visualizes selected metrics in a **Streamlit** dashboard.

# Tech Stack

- **Python 3.10**
- **PostgreSQL 15** (Dockerized)
- **SQLAlchemy & Pandas** for ETL
- **Streamlit** for dashboarding
- **Plotly Express** for interactive charts
- **Docker** + `docker-compose` for reproducible environments

---

# Project Structure

```
dmlab/
├── app/
│   ├── etl_pipeline.py              # Runs the ETL and writes to the DB
│   └── dashboard/
│       └── streamlit.py             # Interactive Streamlit app
├── src/
│   ├── database.py                  # DB engine and metadata
│   └── etl/
│       ├── companies.py             # Company schema + yfinance metadata fetcher
│       ├── daily_prices.py          # Price data fetcher
│       └── metrics.py               # MA, RSI, MACD calculations
├── docker/
│   ├── Dockerfile                   # Python container setup
│   └── docker-compose.yml           # PostgreSQL setup
├── .env                             # DB environment config
├── requirements.txt                 # Python dependencies
└── README.md                        # Project instructions
```
# Environment Variables
All DB credentials are handled via .env.

# Environment Variables
Make sure Docker and Docker Compose are installed on your system.

# 1. Clone the project
```
git clone https://github.com/antalbalint97/dmlab
```

# 2. Start the container
```
docker compose -f docker/docker-compose.yml up --build
```

This will:

-Launch a PostgreSQL container
-Install all Python requirements

# 3. Run the ETL process
```
python -m app.etl_pipeline
```
This will:

-Run the ETL pipeline (app.etl_pipeline.py)
-Populate the database with:
    companies
    daily_prices
    daily_prices_adjusted

You should see logs confirming table creations.

# 4. Launch the dashboard
```
streamlit run app/dashboard/streamlit.py
```

This will:

-Launch the dashboard on a local port, probably: http://localhost:8501