# history.py - hiển thị lịch sử và thống kê
import os
import json
import pandas as pd
import streamlit as st

def load_records(folder="data/records"):
    records = []
    for file in os.listdir(folder):
        if file.endswith(".json"):
            with open(os.path.join(folder, file)) as f:
                records.append(json.load(f))
    return pd.DataFrame(records)

def show_user_history(username):
    df = load_records()
    user_df = df[df['user'] == username]
    if user_df.empty:
        st.info("Chưa có chuẩn đoán nào.")
    else:
        st.subheader("Lịch sử chuẩn đoán")
        st.dataframe(user_df)

def show_area_statistics():
    df = load_records()
    if df.empty:
        st.info("Chưa có dữ liệu thống kê.")
    else:
        st.subheader("Thống kê khu vực có bệnh")
        st.bar_chart(df['location'].value_counts())
