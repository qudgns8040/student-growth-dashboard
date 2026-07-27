import streamlit as st
import pandas as pd

# -------------------------------
# 데이터 불러오기
# -------------------------------

students = pd.read_csv("data/students.csv")
dt_scores = pd.read_csv("data/dt_scores.csv")

# 학생 정보 + DT 점수 병합
df = pd.merge(
    dt_scores,
    students,
    on="student_id",
    how="left"
)

# 날짜 형식 변환
df["date"] = pd.to_datetime(df["date"])

# -------------------------------
# 페이지 제목
# -------------------------------

st.title("학생 현황")

# -------------------------------
# 학생 선택
# -------------------------------

student = st.selectbox(
    "학생 선택",
    sorted(df["name"].unique())
)

# 선택한 학생 데이터
student_df = df[df["name"] == student]

# 학생 기본 정보
student_info = student_df.iloc[0]

# -------------------------------
# 기본 정보
# -------------------------------

st.subheader("기본 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("**이름**")
    st.write(student_info["name"])

with col2:
    st.write("**학년**")
    st.write(student_info["age"])

with col3:
    st.write("**반**")
    st.write(student_info["class"])

# -------------------------------
# 개인 통계
# -------------------------------

st.subheader("개인 통계")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "평균 점수",
        f"{student_df['score'].mean():.1f}"
    )

with col2:
    st.metric(
        "최고 점수",
        int(student_df["score"].max())
    )

with col3:
    st.metric(
        "최저 점수",
        int(student_df["score"].min())
    )

# -------------------------------
# 최근 시험 5회
# -------------------------------

st.subheader("최근 시험 5회")

recent = (
    student_df
    .sort_values("date", ascending=False)
    .head(5)
)

st.dataframe(
    recent[
        [
            "date",
            "dt_type",
            "score"
        ]
    ],
    use_container_width=True,
    hide_index=True
)