import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st

st.set_page_config(
    page_title="Energy Prediction AI",
    page_icon="⚡",
    layout="centered"
)

translations = {
    "th": {
        "app_title": "⚡ ระบบพยากรณ์การใช้พลังงานไฟฟ้าอัจฉริยะ",
        "app_desc": "แอปพลิเคชันต้นแบบสำหรับคาดการณ์การใช้พลังงานไฟฟ้าในบ้าน",
        "input_hour": "ชั่วโมงของวัน (0‑23)",
        "input_temp": "อุณหภูมิ (°C)",
        "predict_btn": "คำนวณการใช้ไฟ",
        "result_text": "คาดการณ์การใช้พลังงาน: {:.2f} กิโลวัตต์‑ชั่วโมง"
    }
}
lang = "th"
txt = translations[lang]

st.title(txt["app_title"])
st.subheader(txt["app_desc"])

X_data = pd.DataFrame({
    "hour": [7,12,18,20,22,9,14,19,21,11],
    "temp": [28,33,31,29,27,26,34,30,28,32]
})
y_data = [1.2,2.5,3.1,2.9,1.8,1.0,2.7,3.0,2.2,2.1]

model = LinearRegression()
model.fit(X_data, y_data)

hour_in = st.number_input(txt["input_hour"], min_value=0, max_value=23, value=12)
temp_in = st.number_input(txt["input_temp"], min_value=15, max_value=45, value=30)

if st.button(txt["predict_btn"]):
    pred = model.predict(pd.DataFrame({"hour":[hour_in], "temp":[temp_in]}))
    st.success(txt["result_text"].format(pred[0]))
