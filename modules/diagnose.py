# diagnose.py - hiện thông tin bệnh
import json
import streamlit as st

def load_disease_info():
    with open("disease_info.json") as f:
        return json.load(f)

def show_disease_info(predicted_class):
    """
    info = load_disease_info()
    if predicted_class in info:
        data = info[predicted_class]
        st.subheader(f"Tên bệnh: {data['name']}")
        st.write("**Mô tả:**", data['description'])
        st.write("**Giải pháp:**", data['solution'])
    else:
        st.warning("Không tìm thấy thông tin bệnh.")
    """
    pass
