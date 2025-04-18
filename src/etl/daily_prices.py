import yfinance as yf
import pandas as pd
from sqlalchemy import insert
from src.database import get_engine, Base


class DailyPrices:
    def __init__(self, ticker: str, start: str, end: str):
        """
        :param ticker: Stock ticker
        :param start: Start date in 'YYYY-MM-DD' format
        :param end: End date in 'YYYY-MM-DD' format
        """
        self.ticker = ticker
        self.start = start
        self.end = end
        self.ticker_obj = yf.Ticker(ticker)
        self.df = self._download_data()

    def _download_data(self) -> pd.DataFrame:
        """Download historical daily price data for the given date range."""
        df = self.ticker_obj.history(start=self.start, end=self.end)
        df.reset_index(inplace=True)  # move 'Date' to column
        df["ticker"] = self.ticker
        return df[["ticker", "Date", "Open", "High", "Low", "Close", "Volume"]]

    def to_dataframe(self) -> pd.DataFrame:
        """Return the full price history as a DataFrame."""
        return self.df.copy()

    def save_to_table(self, session, table_name: str):
        """Insert the data into a dynamically created SQL table."""
        engine = session.bind
        with engine.connect() as conn:
            for _, row in self.df.iterrows():
                record = {
                    "ticker": row["ticker"],
                    "date": row["Date"].date(),
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else None
                }
                stmt = insert(Base.metadata.tables[table_name]).values(**record)
                conn.execute(stmt)
            conn.commit()
