# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import logging
from src.database import get_engine, get_session, DataBase, metadata
from src.etl.daily_prices import DailyPrices
from src.etl.companies import CompanyMetadata
from src.etl.metrics import MetricsCalculator
from sqlalchemy import String, Date, Float, BigInteger
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    filename="etl_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Define the examined companies
faang = ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]
end = datetime.today()
start = end - timedelta(days=365 * 3)
logging.debug(f"Time range: {start.date()} to {end.date()}")

# Initialize the database connection
logging.debug("Initializing database engine and session...")
engine = get_engine()
session = get_session(engine)

# Define the companies schema
columns_companies = {
    "ticker": ((String,), {"unique": True, "nullable": False}),
    "longName": ((String,), {}),
    "sector": ((String,), {}),
    "industry": ((String,), {}),
    "country": ((String,), {}),
    "marketCap": ((BigInteger,), {}),
    "fullTimeEmployees": ((BigInteger,), {}),
    "website": ((String,), {}),
}

logging.debug("Creating 'companies' table...")
DataBase.create_table(engine, "companies", columns_companies)

# Define the daily_prices schema
columns_daily_prices = {
    "ticker": ((String,), {"nullable": False}),
    "date": ((Date,), {"nullable": False}),
    "open": ((Float,), {}),
    "high": ((Float,), {}),
    "low": ((Float,), {}),
    "close": ((Float,), {}),
    "volume": ((BigInteger,), {})
}

logging.debug("Creating 'daily_prices' table...")
DataBase.create_table(engine, "daily_prices", columns_daily_prices)

# Define the daily_prices_adjusted schema
columns_adjusted = {
    "ticker": ((String,), {"nullable": False}),
    "date": ((Date,), {"nullable": False}),
    "open": ((Float,), {}),
    "high": ((Float,), {}),
    "low": ((Float,), {}),
    "close": ((Float,), {}),
    "volume": ((BigInteger,), {}),
    "ma_5": ((Float,), {}),
    "ma_63": ((Float,), {}),
    "ma_126": ((Float,), {}),
    "ma_252": ((Float,), {}),
    "volatility_30d": ((Float,), {}),
    "macd": ((Float,), {}),
    "rsi": ((Float,), {})
}

logging.debug("Creating 'daily_prices_adjusted' table...")
DataBase.create_table(engine, "daily_prices_adjusted", columns_adjusted)

# Loop through each ticker
for ticker in faang:
    logging.info(f"Processing ticker: {ticker}")

    # Save core company metadata
    company = CompanyMetadata(ticker)
    company.save_to_table(session, "companies")
    logging.debug(f"Company metadata saved.")

    # Save raw daily prices
    dp = DailyPrices(ticker, start=start.strftime("%Y-%m-%d"), end=end.strftime("%Y-%m-%d"))
    dp.save_to_table(session, "daily_prices")
    logging.debug(f"Daily prices saved.")

    # Pull, transform and save enriched daily prices
    df = yf.Ticker(ticker).history(start=start, end=end).reset_index()
    df["ticker"] = ticker
    df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    }, inplace=True)

    metrics = MetricsCalculator(df)
    enriched_df = metrics.get_adjusted_table()
    logging.debug("Metrics calculated.")

    with engine.connect() as conn:
        records = enriched_df.to_dict(orient="records")
        conn.execute(metadata.tables["daily_prices_adjusted"].insert(), records)
        conn.commit()
        logging.debug("Enriched daily prices inserted into DB.")

# Close DB session
session.close()
logging.info("ETL job completed: All data loaded into 'companies', 'daily_prices', and 'daily_prices_adjusted' tables.")

