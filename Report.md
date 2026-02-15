## 서울시 시영 주차장 혼잡도 예측 및 추천 시스템

<aside>

## 1. 프로젝트 개요

### 1.1 주제 선정 배경

서울시의 차량 수 증가로 인해 공영주차장 만차 문제가 빈번히 발생함. 시민들은 목적지 주변 주차장의 혼잡도를 실시간으로 파악하거나 사전에 예측하기 어려워, 시간과 비용을 낭비하는 경우가 많음. 이에 따라, 서울시 내 차량 운전자들이 겪는 주차 불편을 해소하고자, 실시간 및 미래 혼잡도를 예측하여 빈자리 정보를 제공하는 공영주차장 추천 시스템을 개발하고자 함

---

### 1.2 주요 기능

- **실시간 주차장 추천 기능**: 사용자의 현재 위치(주소)를 기준으로 가까운 공영 주차장 3곳을 실시간 빈자리 기준으로 추천
- **예측 기반 추천 기능**: 사용자가 입력한 주소 및 날짜/시간에 따라 향후 7일 이내 예측된 혼잡도를 기준으로 가까운 공영주차장 3곳 추천
- **요금 및 상세 정보 제공**: 주차장 위치(주소), 요금 정보, 운영 시간, 전화번호 등 상세 정보를 함께 제공
</aside>

<aside>

## 2. 데이터 수집

### 2.1 데이터 출처

- 서울 열린 데이터 광장: **서울시 시영주차장 실시간 주차대수 정보 (**공영주차장 기본 정보 + 실시간 주차장 상태 데이터 API)
https://data.seoul.go.kr/dataList/OA-21709/A/1/datasetView.do
- Kakao Maps API (**주소 → 위경도 변환**)
[https://developers.kakao.com](https://developers.kakao.com/)

---

### 2.2 데이터 수집 기간

2025.06.09-2025.06.21 (13일간)

---

### 2.3 데이터 수집 방법

- csv파일의 175개 주차장 기본 정보 데이터 수집
- 5분 간격으로 API를 호출하여 Python `requests` 라이브러리를 활용해 실시간 주차 상태 정보를 MySQL 데이터베이스에 저장

---

### 2.4 데이터베이스 설계

MySQL 기반으로 아래와 같이 데이터베이스를 설계

- parknig_lot_info (주차장 기본 정보)
    
    <aside>
    
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
    
- parking_lot_operation (주차장 운영시간 정보)
    
    
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
- parking_lot_fee (주차장 요금 정보)
    
    
    | 컬럼명 | 타입 | 설명 |
    | --- | --- | --- |
    | parking_code | VARCHAR(20) **PK, FK** | 주차장 코드 |
    | basic_fee | INT | 기본 요금 |
    | basic_time | INT | 기본 시간 (분) |
    | extra_fee | INT | 추가 단위 요금 |
    | extra_time | INT | 추가 단위 시간 (분) |
    | daily_max_fee | INT | 일 최대 요금 |
- parking_status (주차장 실시간 상태 정보)
    
    
    | 컬럼명 | 타입 | 설명 |
    | --- | --- | --- |
    | parking_code | VARCHAR(20) **PK, FK** | 주차장 코드 |
    | current_cars | INT | 현재 주차 차량 수 |
    | update_time | DATETIME | 데이터 갱신 시간 |
</aside>

<aside>

## 3. 시스템 구성

### 3.1 기술

- Backend: Python, MySQL, Prophet(시계열 예측), Haversine(거리계산)
- Frontend: Streamlit
- API 활용: Kakao 주소 변환 API, 서울시 공공데이터 API

---

### 3.2 주요 알고리즘 및 로직

- 데이터 전처리:
    - 결측값 보간, 시간 보정, 주차장별 데이터 정렬 등을 통해 예측 정확도 향상,
    - 주소 정보와 주차장 정보가 일치하지 않는 주차장에 대해 UPDATE 문으로 주차장 주소 정보 수정
- 예측 모델: Prophet 라이브러리를 사용해 각 주차장의 시간대별 주차 차량 수 예측
- 거리 계산: Haversine 공식을 사용해 사용자 위치 기준 가장 가까운 주차장 계산
</aside>

<aside>

## 4. 구현

### 4.1 실시간 추천 탭

- 사용자 주소 입력 → 위경도 변환 → DB에서 실시간 주차 상태 조회 → 거리순 정렬 → 3개 주차장 추천 및 해당 주차장 상세 정보 제공

---

### 4.2 예측 기반 추천 탭

- 사용자 주소 + 예측 날짜/시간 입력 → Prophet 모델 기반 예측 → 거리순 정렬 → 3개 주차장 추천 및 해당 주차장 상세 정보 제공
</aside>

<aside>

## 5. 결과 및 기대 효과

- 사용자 입장에서는 혼잡한 도심 내에서도 사전에 예측 가능한 주차 정보를 제공받음으로써 시간 절약 및 스트레스 감소 가능
- 공공 데이터 활용 사례로서 시민과 행정 모두에게 유용한 스마트 도시 서비스 기반 제공
</aside>

<aside>

## 6. 향후 발전 방향

- 모바일 앱 확장: Streamlit기반으로 한 시스템을 모바일 앱 형태로 배포하여 사용자 접근을 용이하게 함
- 실시간 교통량 및 날씨 정보 반영: 예측 정확도 향상을 위해 외부 환경 정보 추가
- 사용자 행동 로그 기반 개인화 추천: 사용자의 주차 이력 데이터를 저장하여 맞춤형 추천 서비스 제공
</aside>
