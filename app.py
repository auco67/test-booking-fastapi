import streamlit as st
import datetime
import random
import requests

choice = st.sidebar.radio("",["ユーザー","会議室","予約"])

if choice == "ユーザー":

    st.title("ユーザー（テスト）")

    with st.form(key="user"):
        user_id: int = random.randint(0,10)
        user_name: str = st.text_input(label="ユーザー名",max_chars=12)
        data = {
            "user_id": user_id,
            "user_name": user_name
        }
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("## 送信データ ##")
        st.json(data)
        st.write("## レスポンス結果 ##")
        url = "http://127.0.0.1:8000/users"
        res = requests.post(url, json=data)
        st.write(res.status_code)
        st.json(res.json())

elif choice == "会議室":

    st.title("会議室（テスト）")

    with st.form(key="room"):
        room_id: int = random.randint(0,10)
        room_name: str = st.text_input(label="会議室名",max_chars=12)
        capacity: int = st.number_input(label="要員",step=1)
        data = {
            "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("## 送信データ ##")
        st.json(data)
        st.write("## レスポンス結果 ##")
        url = "http://127.0.0.1:8000/room"
        res = requests.post(url, json=data)
        st.write(res.status_code)
        st.json(res.json())

elif choice == "予約":

    st.title("予約（テスト）")

    with st.form(key="room"):
        booking_id: int = random.randint(0,10)
        user_id: int = random.randint(0,10)
        room_id: int = random.randint(0,10)
        booked_num: int = st.number_input(label="予約人数",step=1)
        date = st.date_input(label="日付", min_value=datetime.datetime.today())
        start_time = st.time_input(label="開始時刻", value=datetime.time(hour=9,minute=0))
        end_time = st.time_input(label="終了時刻", value=datetime.time(hour=20,minute=0))
        data = {
            "booking_id": booking_id,
            "user_id": user_id,
            "room_id": room_id,
            "book_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat()
        }
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("## 送信データ ##")
        st.json(data)
        st.write("## レスポンス結果 ##")
        url = "http://127.0.0.1:8000/booking"
        res = requests.post(url, json=data)
        st.write(res.status_code)
        st.json(res.json())