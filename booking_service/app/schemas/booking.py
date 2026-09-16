from pydantic import BaseModel, ConfigDict, Field
from app.models.booking import BookingStatus

from datetime import date, datetime
from decimal import Decimal

class BookingBase(BaseModel):
    check_in: date = Field(
        ...
    )
    check_out: date = Field(
        ...
    )

class BookingCreate(BookingBase):
    room_id: int

class BookingResponse(BookingBase):
    id: int
    room_id: int
    user_id: int    
    total_price: Decimal
    status: BookingStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class BookingUpdate(BaseModel):
    status: BookingStatus | None = Field(default=None)