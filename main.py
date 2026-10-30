import os
import pandas as pd
from src.data_collector import DataCollector
from src.volatility_drag import VolatilityDragCalculator
from src.dcf_model import DCFModel
from src.market_pressure import MarketPressureAnalyzer
from src.predictor import MarketPredictor

def main():
    print("==================================================")
    print(" [Macro-Quant-Analyzer] 10/25 ~ 10/31 정밀 검증 및 11월 1주차 예측")
    print("==================================================")
    
    start_date = '2026-10-25'
    end_date = '2026-10-31'
    os.makedirs('output', exist_ok=True)
    
    # 1. 데이터 수집
    collector = DataCollector(start_date=start_date, end_date=end_date)
    raw_data = collector.fetch_all()
    
    # 2. 레버리지 복리 마모 정밀 검증
    print("\n[*] 레버리지 Volatility Drag 정밀 검증 중...")
    drag_calc = VolatilityDragCalculator(raw_data)
    df_drag = drag_calc.analyze()
    df_drag.to_csv('output/volatility_drag_verified.csv', index=False, encoding='utf-8-sig')
    print(df_drag.to_string(index=False))
    
    # 3. DCF 할인율 민감도 정밀 검증
    print("\n[*] DCF 밸류에이션 민감도 공식 연산 중...")
    dcf = DCFModel(raw_data)
    df_dcf = dcf.evaluate()
    df_dcf.to_csv('output/dcf_sensitivity_verified.csv', index=False, encoding='utf-8-sig')
    print(df_dcf.to_string(index=False))
    
    # 4. 시장 압력 진단
    print("\n[*] 시장 압력(VIX) 진단 중...")
    pressure = MarketPressureAnalyzer(raw_data)
    df_pressure = pressure.analyze()
    df_pressure.to_csv('output/market_pressure_verified.csv', index=False, encoding='utf-8-sig')
    print(df_pressure.to_string(index=False))
    
    # 5. 차주 전망 예측
    print("\n[*] 11월 1주차 지수 밴드 예측 중...")
    predictor = MarketPredictor(start_date=start_date, end_date=end_date)
    targets = {'S&P 500': '^GSPC', 'NASDAQ': '^IXIC', 'TQQQ': 'TQQQ', 'SOXL': 'SOXL'}
    forecast_list = []
    
    for name, ticker in targets.items():
        res = predictor.forecast_next_week(ticker)
        res['Asset Name'] = name
        forecast_list.append(res)
        
    df_forecast = pd.DataFrame(forecast_list)
    df_forecast.to_csv('output/forecast_2026_nov_week1.csv', index=False, encoding='utf-8-sig')
    print(df_forecast.to_string(index=False))
    
    print("\n[성공] 모든 정밀 검증 및 예측 결과가 output 폴더에 저장되었습니다.")

if __name__ == '__main__':
    main()
