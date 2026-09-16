from pydantic import BaseModel, ConfigDict, Field


class HotelBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Hotel name",
    )
    description: str | None = Field(
        default=None,
        max_length=1000,
        description="Hotel description",
    )


class HotelCreate(HotelBase):
    pass


class HotelResponse(HotelBase):
    id: int
    slug: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Hotel slug",
    )

    model_config = ConfigDict(from_attributes=True)


class HotelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=100)
    slug: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=1000)