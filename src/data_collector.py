import pandas as pd
import yfinance as yf

class DataCollector:
    def __init__(self, start_date='2026-10-25', end_date='2026-10-31'):
        self.start_date = start_date
        self.end_date = end_date
        self.tickers = {
            'S&P500': '^GSPC',
            'NASDAQ': '^IXIC',
            'VIX': '^VIX',
            'US10Y': '^TNX',
            'TQQQ': 'TQQQ',
            'SOXL': 'SOXL'
        }

    def fetch_all(self):
        data = {}
        for name, ticker in self.tickers.items():
            df = yf.download(ticker, start=self.start_date, end='2026-11-01', progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.loc[self.start_date:self.end_date]
            data[name] = df
        return data
