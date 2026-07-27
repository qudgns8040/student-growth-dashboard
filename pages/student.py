#학생 정보

import streamlit as st
import pandas as pd

st.title("학생 현황")

df = pd.read_csv("data/dt_scores.csv")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("평균 점수", f"{df['score'].mean():.1f}")

with col2:
    st.metric("최고 점수", int(df["score"].max()))

with col3:
    st.metric("최저 점수", int(df["score"].min()))

st.subheader("기초 통계")

st.dataframe(df["score"].describe().to_frame())