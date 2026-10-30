import pandas as pd
import numpy as np
import yfinance as yf

class MarketPredictor:
    def __init__(self, start_date='2026-10-25', end_date='2026-10-31'):
        self.start_date = start_date
        self.end_date = end_date
        
    def forecast_next_week(self, ticker):
        df = yf.download(ticker, start=self.start_date, end='2026-11-01', progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df.loc[self.start_date:self.end_date]
        
        base_price = float(df['Close'].iloc[-1])
        daily_returns = df['Close'].pct_change().dropna()
        mean_ret = float(daily_returns.mean())
        vol = float(daily_returns.std())
        
        np.random.seed(42)
        simulations = 1000
        projected_paths = [base_price * np.prod(1 + np.random.normal(mean_ret, vol, 5)) for _ in range(simulations)]
        
        return {
            'Ticker': ticker,
            'Base Price (10/31)': round(base_price, 2),
            'Expected Price (11/7)': round(float(np.mean(projected_paths)), 2),
            'Upper Bound (+1σ)': round(float(np.percentile(projected_paths, 84.1)), 2),
            'Lower Bound (-1σ)': round(float(np.percentile(projected_paths, 15.9)), 2)
        }
