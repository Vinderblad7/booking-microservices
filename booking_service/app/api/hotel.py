from fastapi import APIRouter, status

from app.schemas.hotel import HotelCreate, HotelResponse, HotelUpdate
from app.api.dependencies import HotelServiceDep


router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=list[HotelResponse])
async def get_hotels(hotel_service: HotelServiceDep):
    return await hotel_service.get_all()


@router.get("/{hotel_id}", response_model=HotelResponse)
async def get_hotel_by_id(
    hotel_id: int,
    hotel_service: HotelServiceDep,
):
    return await hotel_service.get_by_id(hotel_id)


@router.get("/by-slug/{slug}", response_model=HotelResponse)
async def get_hotel_by_slug(
    slug: str,
    hotel_service: HotelServiceDep,
):
    return await hotel_service.get_by_slug(slug)


@router.post("", response_model=HotelResponse, status_code=status.HTTP_201_CREATED)
async def create_hotel(
    hotel_data: HotelCreate,
    hotel_service: HotelServiceDep,
):
    return await hotel_service.create(hotel_data)


@router.patch("/{hotel_id}", response_model=HotelResponse)
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelUpdate,
    hotel_service: HotelServiceDep,
):
    return await hotel_service.update(hotel_id, hotel_data)


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    hotel_id: int,
    hotel_service: HotelServiceDep,
):
    await hotel_service.delete(hotel_id)