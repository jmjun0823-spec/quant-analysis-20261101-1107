import pandas as pd

class MarketPressureAnalyzer:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def analyze(self):
        vix_df = self.raw_data.get('VIX')
        vix_val = float(vix_df['Close'].iloc[-1]) if vix_df is not None and not vix_df.empty else 20.0
        status = "High Volatility Caution" if vix_val > 20 else "Stable Range"
        
        return pd.DataFrame([{
            'VIX Close': round(vix_val, 2),
            'Market Pressure Status': status
        }])
