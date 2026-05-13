import datetime
from pydantic import BaseModel, Field, ConfigDict

class BookingBaseModel(BaseModel):
    user_id: int
    room_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

class Booking(BookingBaseModel):
    booking_id: int

    model_config = ConfigDict(from_attributes=True)

class UserBaseModel(BaseModel):
    user_name: str = Field(max_length=12)

class User(UserBaseModel):
    user_id: int

    model_config = ConfigDict(from_attributes=True)

class RoomBaseModel(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int

class Room(RoomBaseModel):
    room_id: int

    model_config = ConfigDict(from_attributes=True)