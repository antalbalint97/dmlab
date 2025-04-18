import yfinance as yf
import pandas as pd
from sqlalchemy import insert
from src.database import get_engine, Base

class CompanyMetadata:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.ticker_obj = yf.Ticker(ticker)
        self.info = self.ticker_obj.info

    def get_core_metadata(self) -> dict:
        """Get metadata from the API in dictionary form."""
        return {
            "ticker": self.ticker,
            "longName": self.info.get("longName"),
            "sector": self.info.get("sector"),
            "industry": self.info.get("industry"),
            "country": self.info.get("country"),
            "marketCap": self.info.get("marketCap"),
            "fullTimeEmployees": self.info.get("fullTimeEmployees"),
            "website": self.info.get("website"),
        }

    def to_dataframe(self) -> pd.DataFrame:
        """Return a single-row DataFrame for display/debugging."""
        data = self.get_core_metadata()
        return pd.DataFrame([data])

    def save_to_table(self, session, table_name: str):
        """Save the extracted data to a dynamically created table."""
        data = self.get_core_metadata()
        engine = session.bind
        with engine.connect() as conn:
            stmt = insert(Base.metadata.tables[table_name]).values(**data)
            conn.execute(stmt)
            conn.commit()
