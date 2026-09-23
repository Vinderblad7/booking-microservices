from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class RoomBase(BaseModel):
    hotel_id: int
    number: str = Field(..., max_length=20, description="Номер или название комнаты")
    price: Decimal = Field(..., gt=0, description="Цена за ночь")
    capacity: int = Field(default=2, gt=0, description="Вместимость (человек)")


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    number: str | None = Field(default=None, max_length=20)
    price: Decimal | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, gt=0)


class RoomResponse(RoomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)