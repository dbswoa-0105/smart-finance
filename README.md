# 💰 스마트 가계부 (Smart Finance Manager)

Streamlit과 SQLite를 활용하여 만든 쉽고 직관적인 파이썬 웹 가계부 애플리케이션입니다. 

## 🌟 주요 기능
- 내역 관리: 수입 및 지출 내역 간편 추가, 수정, 삭제
- 대시보드: 총 수입, 지출, 현재 잔액을 한눈에 파악
- 데이터 시각화: - 카테고리별 지출 비중 분석 (Bar Chart)
  - 일자별 자금 흐름 파악 (Line Chart)
- 상세 내역 확인: 전체 데이터 표(DataFrame) 제공

## 🛠️ 기술 스택
- **Language:** Python
- **Frontend/Framework:** Streamlit
- **Data/DB:** Pandas, SQLite3

## 🚀 실행 방법

### 1. 필요 라이브러리 설치
터미널을 열고 아래 명령어를 입력하여 필수 패키지를 설치합니다.
```bash
pip install streamlit pandas

설치가 완료되면, 아래 명령어를 통해 웹 환경에서 가계부를 실행합니다.
streamlit run app.py
