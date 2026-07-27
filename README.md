
# 학생 성장 대시보드

수학 학원 학생 데이터를 기반으로 학습 현황과 성장 추이를 분석하고 시각화하는 Streamlit 기반 데이터 분석 프로젝트입니다.

## 프로젝트 소개

학생별 PDT(일일 테스트), 숙제 수행 현황, 진도 데이터를 활용하여

- 학생별 학습 현황 확인
- 성적 변화 추이 분석
- 취약 영역 파악
- 학급 단위 학습 관리

를 지원하는 대시보드를 제작하는 프로젝트입니다.

## 개발 목적

수학 학원 강사 업무 경험을 바탕으로,
반복적으로 관리되는 학생 데이터를 데이터 분석 관점에서 구조화하고

학생 성장 과정을 한눈에 확인할 수 있는 분석 시스템을 구현하는 것을 목표로 합니다.

## 주요 기능 (예정)

- 학생 기본 정보 관리
- 학급별 학생 현황 조회
- PDT 성적 분석
- 학생별 성장 추이 시각화
- 취약 단원 분석
- 학급별 학습 성과 비교

## 기술 스택

### Data Analysis
- Python
- Pandas
- NumPy

### Visualization
- Plotly

### Dashboard
- Streamlit

### Development Environment
- Jupyter Notebook
- VS Code
- Git / GitHub

## 프로젝트 구조
학생성장대시보드/

├── app.py
├── requirements.txt
├── README.md
│
├── notebooks/
│ ├── 01_data.ipynb
│ ├── 02_analysis.ipynb
│ └── 03_dashboard_test.ipynb
│
├── data/
└── assets/


## 실행 방법

### 1. 라이브러리 설치

```bash
pip install -r requirements.txt