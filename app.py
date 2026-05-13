import streamlit as st
import datetime
import requests
import pandas as pd

# ユーザー一覧取得
url_users = "http://127.0.0.1:8000/users"
res = requests.get(url_users)
users = res.json()
df_user = pd.DataFrame(users)
df_user.columns = ["ユーザー名","ユーザーID"]

# Dict型設定（Key：ユーザー名、value:ユーザーID）
dt_users_name = {}
for user in users:
    dt_users_name[user["user_name"]] = user["user_id"]

# Dict型設定（Key：ユーザーID、value:ユーザー名）
dt_users_id = {}
for user in users:
    dt_users_id[user["user_id"]] = user["user_name"]

# 会議室一覧取得
url_rooms = "http://127.0.0.1:8000/rooms"
res = requests.get(url_rooms)
rooms = res.json()
df_room = pd.DataFrame(rooms)
df_room.columns = ["会議名","定員","会議室ID"]

#Dict型設定（Key:会議室名、value:会議室ID）
dt_rooms_name = {}
for room in rooms:
    dt_rooms_name[room["room_name"]] = {
        "room_id":room["room_id"],
        "capacity":room["capacity"]
    }

#Dict型設定（Key:会議室ID、value:会議室名）
dt_rooms_id = {}
for room in rooms:
    dt_rooms_id[room["room_id"]] = {
        "room_name":room["room_name"],
        "capacity":room["capacity"]
    }

# 会議室予約一覧取得
url_bookings = "http://127.0.0.1:8000/bookings"
res = requests.get(url_bookings)
bookings = res.json()

df_bookings = pd.DataFrame(bookings)

# df_bookingsのIDをNAMEに、ISO形式文字列をdatetime型に変換する関数を設定する
to_user_name = lambda x: dt_users_id[x]
to_room_name = lambda x: dt_rooms_id[x]["room_name"]
to_datetime = lambda x: datetime.datetime.fromisoformat(x).strftime("%Y/%m%d %H:%M")

# df_bookingsに適用
df_bookings["user_id"] = df_bookings["user_id"].map(to_user_name)
df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
df_bookings["start_datetime"] = df_bookings["start_datetime"].map(to_datetime)
df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)

# カラム名を変更
df_bookings = df_bookings.rename(
    columns={
        "user_id":"ユーザー名",
        "room_id":"会議室名",
        "booked_num":"予約人数",
        "start_datetime":"開始時刻",
        "end_datetime":"終了時刻",
        "booking_id":"予約ID"
    }
)

choice = st.sidebar.radio("選択", ["ユーザー","会議室","会議室予約"])

if choice == "ユーザー":

    st.title("ユーザー登録画面")
    st.dataframe(data=df_user)

    with st.form(key="user"):
        user_name: str = st.text_input(label="ユーザー名",max_chars=12)
        data = {
            "user_name": user_name
        }
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("## 送信データ ##")
        st.json(data)
        st.write("## レスポンス結果 ##")
        url = "http://127.0.0.1:8001/user"
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        st.write(res.status_code)
        st.json(res.json())

elif choice == "会議室":

    st.title("会議室登録画面")
    st.dataframe(data=df_room)

    with st.form(key="room"):
        room_name: str = st.text_input(label="会議室名",max_chars=12)
        capacity: int = st.number_input(label="定員",step=1, min_value=1)
        data = {
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label="送信")

    if submit_button:
        st.write("## 送信データ ##")
        st.json(data)
        st.write("## レスポンス結果 ##")
        url = "http://127.0.0.1:8001/room"
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.success("会議室登録完了")
        st.write(res.status_code)
        st.json(res.json())

elif choice == "会議室予約":

    st.title("会議室予約画面")
    st.dataframe(data=df_bookings)

    with st.form(key="room"):
        user_name: str = st.selectbox("予約者名",dt_users_name.keys())
        room_name: str = st.selectbox("会議室名",dt_rooms_name.keys())
        booked_num: int = st.number_input(label="予約人数",step=1, min_value=1)
        date = st.date_input(label="日付", min_value=datetime.datetime.today())
        start_time = st.time_input(label="開始時刻", value=datetime.time(hour=9,minute=0))
        end_time = st.time_input(label="終了時刻", value=datetime.time(hour=20,minute=0))
        submit_button = st.form_submit_button(label="送信")

    # 送信ボタン押下時
    if submit_button:
        user_id: int = dt_users_name[user_name]
        room_id: int = dt_rooms_name[room_name]["room_id"]
        capacity: int = dt_rooms_name[room_name]["capacity"]
        start_datetime = datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=start_time.hour,
            minute=start_time.minute
        ).isoformat()
        end_datetime = datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=end_time.hour,
            minute=end_time.minute
        ).isoformat()

        data = {
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": start_datetime,
            "end_datetime": end_datetime
        }

        # 定員以上の予約人数の場合
        if booked_num > capacity:
            st.error(f"{room_name}の定員{capacity}名以上では予約できません。")

        # 開始時刻>=終了時刻の場合
        elif start_time >= end_time:
            st.error("終了時刻より開始時刻を遅く設定することはできません")

        # 予約可能時間（9:00～20:00）を外れた場合
        elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
            st.error("予約可能時間は9:00～20:00です")

        else:
            # 会議室を予約する
            url = "http://127.0.0.1:8000/booking"
            res = requests.post(url, json=data)
            if res.status_code == 200:
                st.success("会議室予約登録完了")
            elif res.status_code == 404 and res.json()["detail"] == "Already booked.":
                st.error("指定の時間は既に予約がは存在します")
