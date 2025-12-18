import streamlit as st
import pandas as pd
from datetime import date

st.title("💸 개인 소비 분석 대시보드")

# 데이터 불러오기
try:
    df = pd.read_csv("spending.csv")
except:
    df = pd.DataFrame(columns=["date", "category", "amount"])

st.subheader("📝 소비 기록 입력")

with st.form("input_form"):
    spend_date = st.date_input("날짜", value=date.today())
    category = st.selectbox("소비 항목", ["식비", "교통", "취미", "기타"])
    amount = st.number_input("금액 (원)", min_value=0, step=1000)
    submitted = st.form_submit_button("추가")

if submitted:
    new_data = pd.DataFrame([[spend_date, category, amount]],
                            columns=["date", "category", "amount"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("spending.csv", index=False)
    st.success("소비 기록이 추가되었습니다!")

# 데이터 타입 정리
if not df.empty:
    df["date"] = pd.to_datetime(df["date"])

    st.subheader("📊 소비 분석 결과")

    st.metric("총 소비 금액", f"{df['amount'].sum():,} 원")

    # 항목별 소비
    category_sum = df.groupby("category")["amount"].sum()
    st.write("### 항목별 소비 비율")
    st.bar_chart(category_sum)

    # 날짜별 소비
    daily_sum = df.groupby("date")["amount"].sum()
    st.write("### 날짜별 소비 변화")
    st.line_chart(daily_sum)

    st.write("### 전체 소비 데이터")
    st.dataframe(df)
else:
    st.info("아직 소비 기록이 없습니다.")
