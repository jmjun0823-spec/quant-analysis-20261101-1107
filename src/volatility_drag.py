import pandas as pd
import numpy as np

class VolatilityDragCalculator:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def analyze(self):
        """
        Volatility Drag 공식 검증:
        지수 일간 변동성(sigma)에 따른 3배 레버리지 상품의 이론적 복리 마모(Drag) 산출
        Drag ≈ -0.5 * (L^2 - L) * (sigma^2)
        """
        results = []
        target_assets = {'TQQQ': 'NASDAQ', 'SOXL': 'NASDAQ'}
        
        for asset, benchmark in target_assets.items():
            df = self.raw_data.get(asset)
            if df is not None and not df.empty:
                daily_ret = df['Close'].pct_change().dropna()
                sigma = float(daily_ret.std())
                
                leverage = 3.0
                theoretical_drag_pct = -0.5 * (leverage**2 - leverage) * (sigma**2) * 100 * len(daily_ret)
                
                cum_simple_return = daily_ret.sum() * leverage * 100
                actual_cum_return = ((1 + daily_ret * leverage).prod() - 1) * 100
                compounding_gap = actual_cum_return - cum_simple_return
                
                results.append({
                    'Asset': asset,
                    'Period Volatility (σ, %)': round(sigma * 100, 4),
                    'Theoretical Drag (%)': round(theoretical_drag_pct, 4),
                    'Actual Compounding Gap (%)': round(compounding_gap, 4)
                })
                
        return pd.DataFrame(results)
