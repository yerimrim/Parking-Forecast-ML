- 서울시 시영주차장 실시간 주차대수 정보 (과거 데이터 + API)
    - **전체 데이터 (42개 columns):** 주차장코드, 주차장명, 주소, 주차장 종류, 주차장 종류명, 운영구분, 운영구분명, 전화번호, 주차현황 정보 제공 여부, 주차현황 정보 제공여부명, 총 주차면, 현재 주차 차량수, 현재 주차 차량수 업데이트시간, 유무료구분, 유무료구분명, 야간무료개방여부, 평일 운영 시작시각(HHMM), 평일 운영 종료시각 (HHMM), 주말 운영 시작시각 (HHMM), 주말 운영 종료시각 (HHMM), 공휴일 운영 시작시각 (HHMM), 공휴일 운영 종료시각 (HHMM), 토요일 유,무료 구분, 토요일 유,무료 구분명, 공휴일 유,무료 구분, 공휴일 유,무료 구분명, 월 정기권 금액, 노상 주차장 관리그룹번호, 기본 주차 요금, 기본 주차 시간(분 단위), 추가 단위 요금, 추가 단위 시간(분 단위), 버스 기본 주차 요금, 버스 기본 주차 시간(분 단위), 버스 추가 단위 요금, 버스 추가 단위 시간(분 단위), 일 최대 요금, 공유 주차장 관리업체명, 공유 주차장 여부, 공유 주차장 관리 업체 링크, 공유 주차장 기타사항
    - **사용 데이터:** 주차장코드, 주차장명, 주소, 주차장 종류명, 운영구분명, 전화번호, 주차현황 정보 제공여부명, 총 주차면, 현재 주차 차량수, 현재 주차 차량수 업데이트시간, 유무료구분, 유무료구분명, 야간무료개방여부, 평일 운영 시작시각(HHMM), 평일 운영 종료시각 (HHMM), 주말 운영 시작시각 (HHMM), 주말 운영 종료시각 (HHMM), 공휴일 운영 시작시각 (HHMM), 공휴일 운영 종료시각 (HHMM), 토요일 유,무료 구분명, 공휴일 유,무료 구분명, 기본 주차 요금, 기본 주차 시간(분 단위), 추가 단위 요금, 추가 단위 시간(분 단위), 일 최대 요금
        
        [서울시 시영주차장 실시간 주차대수 정보](https://data.seoul.go.kr/dataList/OA-21709/A/1/datasetView.do)


---

- Table Structure Overview
  <aside>

### parking_lot_info

| 컬럼명 | 타입 | 설명 |
| --- | --- | --- |
| parking_code | VARCHAR(20) **PK** | 주차장 코드 |
| name | VARCHAR(100) | 주차장명 |
| address | VARCHAR(200) | 주소 |
| type_name | VARCHAR(50) | 주차장 종류명 |
| operation_type_name | VARCHAR(50) | 운영구분명 |
| phone | VARCHAR(20) | 전화번호 |
| info_provide_name | VARCHAR(255) | 주차현황 정보 제공여부명 |
| total_spots | INT | 총 주차면 |
| fee_type_name | VARCHAR(20) | 유/무료 구분명 |
| night_free_name | VARCHAR(10) | 야간무료개방여부명 |
| latitude | DOUBLE | 위도 |
| longitude | DOUBLE | 경도 |
</aside>

<aside>

### parking_lot_operation

| 컬럼명 | 타입 | 설명 |
| --- | --- | --- |
| parking_code | VARCHAR(20) **PK, FK** | 주차장 코드 |
| weekday_start | VARCHAR(4) | 평일 시작시각 (HHMM) |
| weekday_end | VARCHAR(4) | 평일 종료시각 (HHMM) |
| weekend_start | VARCHAR(4) | 주말 시작시각 (HHMM) |
| weekend_end | VARCHAR(4) | 주말 종료시각 (HHMM) |
| holiday_start | VARCHAR(4) | 공휴일 시작시각 (HHMM) |
| holiday_end | VARCHAR(4) | 공휴일 종료시각 (HHMM) |
| sat_fee_type_name | VARCHAR(20) | 토요일 유무료 구분명 |
| holiday_fee_type_name | VARCHAR(20) | 공휴일 유무료 구분명 |
</aside>

<aside>

### parking_lot_fee

| 컬럼명 | 타입 | 설명 |
| --- | --- | --- |
| parking_code | VARCHAR(20) **PK, FK** | 주차장 코드 |
| basic_fee | INT | 기본 요금 |
| basic_time | INT | 기본 시간 (분) |
| extra_fee | INT | 추가 단위 요금 |
| extra_time | INT | 추가 단위 시간 (분) |
| daily_max_fee | INT | 일 최대 요금 |
</aside>

<aside>

### parking_status

| 컬럼명 | 타입 | 설명 |
| --- | --- | --- |
| parking_code | VARCHAR(20) **PK, FK** | 주차장 코드 |
| current_cars | INT | 현재 주차 차량 수 |
| update_time | DATETIME | 데이터 갱신 시간 |
</aside>

<aside>
