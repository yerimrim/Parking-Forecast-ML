import pandas as pd
import pymysql
from sqlalchemy import create_engine
from datetime import datetime
engine = create_engine("mysql+pymysql://root:happyjyr0324?@localhost:3306/parkingDB")


# parking_lot_info
info_cols = ['주차장코드', '주차장명', '주소', '주차장 종류명', '운영구분명', '전화번호', '주차현황 정보 제공여부명', 
             '총 주차면', '유무료구분명', '야간무료개방여부명']
df_info = df[info_cols].copy()
df_info.columns = ['parking_code', 'name', 'address', 'type_name', 'operation_type_name', 
                   'phone', 'info_provide_name', 'total_spots', 'fee_type_name', 'night_free_name']

# parking_lot_operation
operation_cols = ['주차장코드', '평일 운영 시작시각(HHMM)', '평일 운영 종료시각(HHMM)', 
                  '주말 운영 시작시각(HHMM)', '주말 운영 종료시각(HHMM)', 
                  '공휴일 운영 시작시각(HHMM)', '공휴일 운영 종료시각(HHMM)', 
                  '토요일 유,무료 구분명', '공휴일 유,무료 구분명']
df_op = df[operation_cols].copy()
df_op.columns = ['parking_code', 'weekday_start', 'weekday_end', 'weekend_start', 'weekend_end',
                 'holiday_start', 'holiday_end', 'sat_fee_type_name', 'holiday_fee_type_name']

# parking_lot_fee
fee_cols = ['주차장코드', '기본 주차 요금', '기본 주차 시간(분 단위)', '추가 단위 요금', 
            '추가 단위 시간(분 단위)', '일 최대 요금']
df_fee = df[fee_cols].copy()
df_fee.columns = ['parking_code', 'basic_fee', 'basic_time', 'extra_fee', 'extra_time', 'daily_max_fee']


# 데이터 삽입
df_info.to_sql('parking_lot_info', con=engine, if_exists='append', index=False)
df_op.to_sql('parking_lot_operation', con=engine, if_exists='replace', index=False)
df_fee.to_sql('parking_lot_fee', con=engine, if_exists='replace', index=False)
