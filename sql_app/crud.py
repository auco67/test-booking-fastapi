from typing import Annotated
from fastapi import Query
from .database import SessionDep
from .models import User, Room, Booking
from . import schemas
from sqlmodel import select

# ユーザー一覧取得
def read_users(
        session: SessionDep,
        offset: int=0, 
        limit: Annotated[int,Query(le=100)]= 100,
    ) -> list[schemas.User]:
    users = session.exec(select(schemas.User).offset(offset).limit(limit)).all()
    return users

# 会議室一覧取得
def read_rooms(
        session: SessionDep,
        offset: int=0, 
        limit: Annotated[int,Query(le=100)]= 100,
        ) -> list[schemas.Room]:
        rooms = session.exec(select(schemas.Room).offset(offset).limit(limit)).all()
        return rooms

# 予約一覧取得
def read_bookings(
        session: SessionDep,
        offset: int=0, 
        limit: Annotated[int,Query(le=100)]= 100,
        ) -> list[schemas.Booking]:
        bookings = session.exec(select(schemas.Booking).offset(offset).limit(limit)).all()
        return bookings

# 会議室作成
def create_room(room: Room, session: SessionDep) -> Room:
    db_room = Room(room_name=room.room_name)
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room

# ユーザー作成
def create_user(user: User, session: SessionDep) -> User:
    db_user = User(user_name=user.user_name)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# 予約作成
def create_booking(booking: Booking, session: SessionDep) -> Booking:
    db_booking = Booking(
        user_id=booking.user_id,
        room_id=booking.room_id,
        booked_num=booking.booked_num,
        start_datetime=booking.start_datetime,
        end_datetime=booking.end_datetime)
    session.add(db_booking)
    session.commit()
    session.refresh(db_booking)
    return db_booking