import datetime
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    user_id: int | None = Field(default=None, primary_key=True)
    user_name: str = Field(max_length=12)

    booking: list["User"] = Relationship(back_populates="user", cascade_delete=True)

class Room(SQLModel, table=True):
    room_id: int | None = Field(default=None, primary_key=True)
    room_name: str = Field(max_length=12)
    capacity: int

    booking: list["Room"] = Relationship(back_populates="room", cascade_delete=True)


class Booking(SQLModel, table=True):
    booking_id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.user_id",ondelete="CASCADE")
    room_id: int | None = Field(default=None, foreign_key="room.room_id",ondelete="CASCADE")
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime