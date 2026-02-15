import requests
import pymysql
import time
from datetime import datetime


# API 설정

# DB 설정


# 5분 단위로 반올림
def round_to_5min(dt):
    return dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0)


# API에서 주차장 정보 가져오기
def fetch_parking_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    return data['GetParkingInfo']['row']


# DB 삽입 및 갱신
def insert_or_update_parking_data(data, connection):
    with connection.cursor() as cursor:
        for entry in data:
            parking_code = entry['PKLT_CD']
            try:
                current_cars = int(entry['NOW_PRK_VHCL_CNT'] or 0)
            except:
                current_cars = 0

            update_time_str = entry.get('NOW_PRK_VHCL_UPDT_TM')
            if not update_time_str or not update_time_str.strip():
                continue

            try:
                raw_time = datetime.strptime(update_time_str.strip(), "%Y-%m-%d %H:%M:%S")
                update_time = round_to_5min(raw_time)
            except ValueError:
                print(f"잘못된 시간 형식: {update_time_str}")
                continue

            # 주차장 정보 존재 여부 확인
            cursor.execute("SELECT 1 FROM parking_lot_info WHERE parking_code = %s", (parking_code,))
            exists = cursor.fetchone()

            if not exists:
                # 주차장 기본 정보 INSERT
                cursor.execute("""
                    INSERT INTO parking_lot_info (
                        parking_code, name, address, type_name, operation_type_name,
                        phone, info_provide_name, total_spots, fee_type_name, night_free_name
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    parking_code,
                    entry.get('PKLT_NM'),
                    entry.get('ADDR'),
                    entry.get('PRK_TYPE_NM'),
                    entry.get('OPER_SE_NM'),
                    entry.get('TELNO'),
                    entry.get('PRK_STTS_NM'),
                    int(entry.get('TPKCT') or 0),
                    entry.get('PAY_YN_NM'),
                    entry.get('NGHT_PAY_YN_NM')
                ))

                # 운영시간 INSERT
                cursor.execute("""
                    INSERT INTO parking_lot_operation (
                        parking_code, weekday_start, weekday_end,
                        weekend_start, weekend_end, holiday_start, holiday_end,
                        sat_fee_type_name, holiday_fee_type_name
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    parking_code,
                    entry.get('WD_OPER_BGNG_TM'),
                    entry.get('WD_OPER_END_TM'),
                    entry.get('WE_OPER_BGNG_TM'),
                    entry.get('WE_OPER_END_TM'),
                    entry.get('LHLDY_OPER_BGNG_TM'),
                    entry.get('LHLDY_OPER_END_TM'),
                    entry.get('SAT_CHGD_FREE_NM'),
                    entry.get('LHLDY_CHGD_FREE_SE_NAME')
                ))

                # 요금 정보 INSERT
                cursor.execute("""
                    INSERT INTO parking_lot_fee (
                        parking_code, basic_fee, basic_time,
                        extra_fee, extra_time, daily_max_fee
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    parking_code,
                    int(entry.get('BSC_PRK_CRG') or 0),
                    int(entry.get('BSC_PRK_HR') or 0),
                    int(entry.get('ADD_PRK_CRG') or 0),
                    int(entry.get('ADD_PRK_HR') or 0),
                    int(entry.get('DAY_MAX_CRG') or 0)
                ))

            # parking_code와 current_cars 중복 체크 후 insert
            cursor.execute("""
                SELECT 1 FROM parking_status
                WHERE parking_code = %s AND current_cars = %s
            """, (parking_code, current_cars))
            exists_status = cursor.fetchone()

            if not exists_status:
                cursor.execute("""
                    INSERT INTO parking_status (parking_code, current_cars, update_time)
                    VALUES (%s, %s, %s)
                """, (parking_code, current_cars, update_time))

        connection.commit()


# 메인 실행 함수
def main():
    connection = None
    try:
        print(f"[{datetime.now()}] 데이터 수집 시작")
        data = fetch_parking_data()
        print(f"[{datetime.now()}] 데이터 수집 완료, {len(data)}건")
        connection = pymysql.connect(**DB_CONFIG)
        insert_or_update_parking_data(data, connection)
        print(f"[{datetime.now()}] DB 삽입 완료")
    except Exception as e:
        print("오류 발생:", e)
    finally:
        if connection:
            connection.close()


# 5분 주기로 실행
if __name__ == '__main__':
    while True:
        main()
        time.sleep(300)  # 5분 대기
