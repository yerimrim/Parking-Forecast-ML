# MySQL 데이터 불러오기
import pymysql
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

db_config = {'host': 'localhost',  
             'user': 'root',
             'password': 'happyjyr0324?',
             'database': 'parkingDB',
             'port': 3306}

conn = pymysql.connect(**db_config)

query = """ SELECT id, parking_code, current_cars, update_time 
            FROM parking_status """
df = pd.read_sql(query, conn)
conn.close()


# 전처리 (앞뒤 평균)
df['update_time'] = pd.to_datetime(df['update_time'])
df = df[df['update_time'] >= pd.Timestamp('2025-06-09 19:10:00')].copy()

start_time = pd.Timestamp('2025-06-09 19:10:00')
end_time = df['update_time'].max()

parking_codes = df['parking_code'].unique()
result_df = []

for code in parking_codes:
    tmp = df[df['parking_code'] == code].copy()
    full_time_index = pd.date_range(start=start_time, end=end_time, freq='5T')
    tmp.set_index('update_time', inplace=True)
    tmp = tmp.reindex(full_time_index)
    tmp['parking_code'] = code
    tmp['current_cars'] = tmp['current_cars'].interpolate(method='linear')
    tmp['current_cars'].fillna(method='ffill', inplace=True)
    tmp['current_cars'].fillna(method='bfill', inplace=True)

    tmp.reset_index(inplace=True)
    tmp.rename(columns={'index':'update_time'}, inplace=True)
    result_df.append(tmp)
    
df = pd.concat(result_df, ignore_index=True)
df.reset_index(drop=True, inplace=True)
df['id'] = df.index + 1

# parking_code 별 데이터 개수 확인
counts = df.groupby('parking_code').size().sort_values(ascending=False)
counts = pd.DataFrame(counts)
counts

# 예측 및 성능 확인 (prophet)
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

parking_codes = df['parking_code'].unique()

for code in parking_codes:
    df_code = df[df['parking_code'] == code][['update_time', 'current_cars']].copy()
    df_code.rename(columns={'update_time':'ds', 'current_cars':'y'}, inplace=True)
    
    print(f"\n=== {code} 주차장 공간 예측 및 검증 ===")
    
    tscv = TimeSeriesSplit(n_splits=3) # train 75%, test 25%
    fold_num = 1
    for train_index, test_index in tscv.split(df_code):
        train_df = df_code.iloc[train_index]
        valid_df = df_code.iloc[test_index]
        
        model = Prophet()
        model.fit(train_df)
        
        future = model.make_future_dataframe(periods=len(valid_df), freq='5T')
        forecast = model.predict(future)

        valid_forecast = forecast[-len(valid_df):]
        
        rmse = np.sqrt(mean_squared_error(valid_df['y'], valid_forecast['yhat']))
        print(f"Fold {fold_num} Validation RMSE: {rmse:.2f}")

        plt.figure(figsize=(12,6))
        plt.plot(train_df['ds'], train_df['y'], label='Train')
        plt.plot(valid_df['ds'], valid_df['y'], label='Validation')
        plt.plot(valid_forecast['ds'], valid_forecast['yhat'], label='Forecast')
        plt.fill_between(valid_forecast['ds'], valid_forecast['yhat_lower'], valid_forecast['yhat_upper'], color='pink', alpha=0.3)
        plt.title(f"{code} Fold {fold_num} Forecast vs Actual")
        plt.xlabel('Time')
        plt.ylabel('Current Cars')
        plt.legend()
        plt.show()
        
        fold_num += 1

# 전체 데이터로 예측 (prophet)
import warnings
import logging
warnings.filterwarnings("ignore", category=FutureWarning)
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

df['ds'] = pd.to_datetime(df['update_time'])

parking_codes = df['parking_code'].unique()

for code in parking_codes:
    print(f"\n=== {code} 주차장 공간 예측 ===")
    
    df_code = df[df['parking_code'] == code][['update_time', 'current_cars']].copy()
    df_code.rename(columns={'update_time': 'ds', 'current_cars': 'y'}, inplace=True)

    model = Prophet()
    model.fit(df_code)

    future = model.make_future_dataframe(periods=24, freq='H')  # 7일 예측 (1시간 단위)
    forecast = model.predict(future)

    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    plt.figure(figsize=(10,6))
    plt.plot(df_code['ds'], df_code['y'], label='실제 데이터')
    plt.plot(forecast['ds'], forecast['yhat'], label='예측 값', color='orange')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='orange', alpha=0.3, label='예측 구간')
    plt.title(f"{code} 주차장 공간 예측")
    plt.xlabel("시간")
    plt.ylabel("주차된 차량 수")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
