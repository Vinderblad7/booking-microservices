from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import PaymentStatus


class PaymentBase(BaseModel):
    booking_id: int
    amount: Decimal = Field(..., gt=0)


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    user_id: int
    status: PaymentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaymentUpdate(BaseModel):
    status: PaymentStatus | None = Field(default=None)


class PaymentProcessRequest(BaseModel):
    card_number: str | None = Field(default=None)
