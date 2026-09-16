from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.booking import BookingStatus


class BookingBase(BaseModel):
    check_in: date
    check_out: date

    @model_validator(mode="after")
    def validate_dates(self) -> "BookingBase":
        if self.check_out <= self.check_in:
            raise ValueError("check_out must be strictly after check_in")
        return self


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


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
