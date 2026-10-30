import pandas as pd
import numpy as np

class DCFModel:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def evaluate(self):
        """
        블로그 내 DCF 공식: PV = sum( FCF_t / (1 + r)^t )
        10월 말 기준 10년물 국채 금리(r)의 변화에 따른 기업 가치 민감도를 정밀 계산합니다.
        """
        tnx_df = self.raw_data.get('US10Y')
        if tnx_df is not None and not tnx_df.empty:
            base_rate = float(tnx_df['Close'].iloc[-1]) / 10.0
        else:
            base_rate = 4.25
            
        fcfs = [100, 120, 145, 175, 210]
        terminal_value = 3000
        rate_deltas = [-1.0, -0.5, 0.0, 0.5, 1.0]
        sensitivity_results = []
        
        def calculate_pv(r):
            pv = sum([fcf / ((1 + r/100) ** (t+1)) for t, fcf in enumerate(fcfs)])
            tv_pv = terminal_value / ((1 + r/100) ** len(fcfs))
            return pv + tv_pv

        base_pv = calculate_pv(base_rate)

        for delta in rate_deltas:
            scenario_rate = base_rate + delta
            scenario_pv = calculate_pv(scenario_rate)
            pct_change = ((scenario_pv - base_pv) / base_pv) * 100
            
            sensitivity_results.append({
                '10Y Yield (%)': round(scenario_rate, 2),
                'Rate Delta (%p)': delta,
                'Estimated PV': round(scenario_pv, 2),
                'Valuation Impact (%)': round(pct_change, 2)
            })
            
        return pd.DataFrame(sensitivity_results)
