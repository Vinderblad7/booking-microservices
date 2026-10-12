from sqlalchemy import ForeignKey, String, Text
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.room import Room


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    rooms: Mapped[list["Room"]] = relationship(
        back_populates="hotel", cascade="all, delete-orphan"
    )
    images: Mapped[list["HotelImage"]] = relationship(
        back_populates="hotel", cascade="all, delete-orphan"
    )


class HotelImage(Base):
    __tablename__ = "hotel_images"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(
        ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False
    )
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    key: Mapped[str] = mapped_column(String(255), nullable=False)

    hotel: Mapped["Hotel"] = relationship(back_populates="images")
