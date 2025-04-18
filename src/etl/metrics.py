import pandas as pd

class MetricsCalculator:
    def __init__(self, df: pd.DataFrame):
        """
        df: DataFrame must contain at least a 'ticker', 'date', and 'close' column with daily stock prices.
        """
        self.df = df.copy()

    def daily_return(self):
        self.df['daily_return'] = self.df['close'].pct_change()
        return self.df

    def cumulative_return(self):
        self.df['cumulative_return'] = (1 + self.df['close'].pct_change()).cumprod() - 1
        return self.df

    def moving_averages(self):
        self.df['ma_5'] = self.df['close'].rolling(window=5).mean()
        self.df['ma_63'] = self.df['close'].rolling(window=63).mean()
        self.df['ma_126'] = self.df['close'].rolling(window=126).mean()
        self.df['ma_252'] = self.df['close'].rolling(window=252).mean()
        return self.df

    def volatility(self, window=30):
        self.df[f'volatility_{window}d'] = self.df['close'].pct_change().rolling(window=window).std()
        return self.df

    def macd(self):
        ema_12 = self.df['close'].ewm(span=12, adjust=False).mean()
        ema_26 = self.df['close'].ewm(span=26, adjust=False).mean()
        self.df['macd'] = ema_12 - ema_26
        return self.df

    def rsi(self, window=14):
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        self.df['rsi'] = 100 - (100 / (1 + rs))
        return self.df

    def all_metrics(self):
        self.daily_return()
        self.cumulative_return()
        self.moving_averages()
        self.volatility()
        self.macd()
        self.rsi()
        return self.df

    def get_adjusted_table(self):
        """
        Returns the full adjusted daily prices table suitable for dashboard or export.
        Columns: ticker, date, open, high, low, close, volume, ma_5, ma_63, ma_126, ma_252, volatility_30d, macd, rsi
        """
        self.all_metrics()
        keep_cols = [
            'ticker', 'date', 'open', 'high', 'low', 'close', 'volume',
            'ma_5', 'ma_63', 'ma_126', 'ma_252',
            'volatility_30d', 'macd', 'rsi'
        ]
        return self.df[keep_cols].copy()