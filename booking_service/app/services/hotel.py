from slugify import slugify

from app.exceptions import HotelAlreadyExistsError, HotelNotFoundError
from app.models.hotel import Hotel
from app.repositories.hotel import HotelRepository
from app.schemas.hotel import HotelCreate, HotelUpdate


class HotelService:
    def __init__(self, hotel_repo: HotelRepository):
        self.hotel_repo = hotel_repo

    async def get_all(self) -> list[Hotel]:
        return await self.hotel_repo.get_all()

    async def get_by_id(self, hotel_id: int) -> Hotel:
        hotel = await self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with id {hotel_id} not found")
        return hotel

    async def get_by_slug(self, slug: str) -> Hotel:
        hotel = await self.hotel_repo.get_by_slug(slug)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with slug {slug} not found")
        return hotel

    async def create(self, hotel_data: HotelCreate) -> Hotel:
        slug = slugify(hotel_data.name)

        hotel_exist = await self.hotel_repo.get_by_slug(slug)
        if hotel_exist:
            raise HotelAlreadyExistsError(f"Hotel with slug '{slug}' already exists")

        data = hotel_data.model_dump()
        data["slug"] = slug

        return await self.hotel_repo.create(data)

    async def update(self, hotel_id: int, hotel_data: HotelUpdate) -> Hotel:
        hotel = await self.get_by_id(hotel_id)

        data = hotel_data.model_dump(exclude_unset=True)

        if "name" in data and data["name"] != hotel.name:
            new_slug = slugify(data["name"])

            existing_hotel = await self.hotel_repo.get_by_slug(new_slug)
            if existing_hotel and existing_hotel.id != hotel_id:
                raise HotelAlreadyExistsError(
                    f"Hotel with slug '{new_slug}' already exists"
                )

            data["slug"] = new_slug

        return await self.hotel_repo.update(hotel, data)

    async def delete(self, hotel_id: int) -> None:
        hotel = await self.get_by_id(hotel_id)
        await self.hotel_repo.delete(hotel)