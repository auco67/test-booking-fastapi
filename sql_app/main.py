from typing import List
from sqlmodel import SQLModel
from fastapi import FastAPI
from .schemas import UserBaseModel,User, RoomBaseModel,Room, BookingBaseModel,Booking
from .database import engine, SessionDep
from . import crud

# テーブル作成
SQLModel.metadata.create_all(bind=engine)

# FastAPIアプリケーション初期化
app = FastAPI()

"""
Read
    一覧を取得する
"""
@app.get("/users", response_model=List[User])
async def read_users(session:SessionDep,offset: int=0, limit: int=100):
    return crud.get_users(session=session, offset=offset, limit=limit)

@app.get("/rooms", response_model=List[Room])
async def read_rooms(session:SessionDep, offset: int=0, limit: int=100):
    return crud.get_rooms(session=session, offset=offset, limit=limit)

@app.get("/bookings", response_model=List[Booking])
async def read_bookings(session:SessionDep, offset: int=0, limit: int=100):
    return crud.get_bookings(session=session, offset=offset, limit=limit)

"""
Create
    データを作成する
"""
@app.post("/user", response_model=User)
async def create_user(user: UserBaseModel,session:SessionDep):
    return crud.create_user(user=user, session=session)

@app.post("/room", response_model=Room)
async def create_room(room: RoomBaseModel, session:SessionDep):
    return crud.create_room(room=room, session=session)

@app.post("/booking", response_model=Booking)
async def create_booking(booking: BookingBaseModel,session:SessionDep):
    return crud.create_booking(booking=booking, session=session)