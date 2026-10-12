from fastapi import UploadFile
from slugify import slugify

from app.core.cache import cache
from app.exceptions import HotelAlreadyExistsError, HotelNotFoundError, ImageNotFoundError
from app.redis import redis_client
from app.repositories.hotel import HotelRepository
from app.s3 import s3_client
from app.schemas.hotel import (
    HotelCreate,
    HotelFilter,
    HotelImageResponse,
    HotelResponse,
    HotelUpdate,
)


class HotelService:
    def __init__(self, hotel_repo: HotelRepository):
        self.hotel_repo = hotel_repo

    @cache(expire=300, prefix="hotels:all")
    async def get_all(self, filters: HotelFilter | None = None) -> list[HotelResponse]:
        hotels = await self.hotel_repo.get_all(filters)
        return [HotelResponse.model_validate(h) for h in hotels]

    @cache(expire=300, prefix="hotels:id")
    async def get_by_id(self, hotel_id: int) -> HotelResponse:
        hotel = await self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with id {hotel_id} not found")
        return HotelResponse.model_validate(hotel)

    @cache(expire=300, prefix="hotels:slug")
    async def get_by_slug(self, slug: str) -> HotelResponse:
        hotel = await self.hotel_repo.get_by_slug(slug)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with slug {slug} not found")
        return HotelResponse.model_validate(hotel)

    async def create(self, hotel_data: HotelCreate) -> HotelResponse:
        slug = slugify(hotel_data.name)

        hotel_exist = await self.hotel_repo.get_by_slug(slug)
        if hotel_exist:
            raise HotelAlreadyExistsError(f"Hotel with slug '{slug}' already exists")

        data = hotel_data.model_dump()
        data["slug"] = slug

        created_hotel = await self.hotel_repo.create(data)

        await redis_client.delete_by_pattern("hotels:*")

        return HotelResponse.model_validate(created_hotel)

    async def update(self, hotel_id: int, hotel_data: HotelUpdate) -> HotelResponse:
        hotel = await self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with id {hotel_id} not found")

        data = hotel_data.model_dump(exclude_unset=True)

        if "name" in data and data["name"] != hotel.name:
            new_slug = slugify(data["name"])

            existing_hotel = await self.hotel_repo.get_by_slug(new_slug)
            if existing_hotel and existing_hotel.id != hotel_id:
                raise HotelAlreadyExistsError(
                    f"Hotel with slug '{new_slug}' already exists"
                )

            data["slug"] = new_slug

        updated_hotel = await self.hotel_repo.update(hotel, data)

        await redis_client.delete_by_pattern("hotels:*")

        return HotelResponse.model_validate(updated_hotel)

    async def delete(self, hotel_id: int) -> None:
        hotel = await self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with id {hotel_id} not found")

        for img in hotel.images:
            await s3_client.delete_file(img.key)

        await self.hotel_repo.delete(hotel)
        await redis_client.delete_by_pattern("hotels:*")

    async def upload_image(self, hotel_id: int, file: UploadFile) -> HotelImageResponse:
        hotel = await self.hotel_repo.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundError(f"Hotel with id {hotel_id} not found")

        url, key = await s3_client.upload_file(file, folder=f"hotels/{hotel_id}")
        image = await self.hotel_repo.add_image(hotel_id=hotel_id, url=url, key=key)
        await redis_client.delete_by_pattern("hotels:*")
        return HotelImageResponse.model_validate(image)

    async def delete_image(self, image_id: int) -> None:
        image = await self.hotel_repo.get_image_by_id(image_id)
        if not image:
            raise ImageNotFoundError(f"Image with id {image_id} not found")

        await s3_client.delete_file(image.key)
        await self.hotel_repo.delete_image(image)
        await redis_client.delete_by_pattern("hotels:*")