from fastapi import APIRouter, Query, status

from app.api.dependencies import CurrentUserIdDep, PaymentServiceDep
from app.schemas.payment import (
    PaymentCreate,
    PaymentProcessRequest,
    PaymentResponse,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("", response_model=list[PaymentResponse])
async def get_payments(
    payment_service: PaymentServiceDep,
    user_id: int | None = Query(default=None),
    booking_id: int | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
):
    return await payment_service.get_all(
        user_id=user_id,
        booking_id=booking_id,
        skip=skip,
        limit=limit,
    )


@router.get("/my", response_model=list[PaymentResponse])
async def get_my_payments(
    payment_service: PaymentServiceDep,
    user_id: CurrentUserIdDep,
):
    return await payment_service.get_all(user_id=user_id)


@router.get("/booking/{booking_id}", response_model=PaymentResponse)
async def get_payment_by_booking_id(
    booking_id: int,
    payment_service: PaymentServiceDep,
):
    return await payment_service.get_by_booking_id(booking_id=booking_id)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(
    payment_id: int,
    payment_service: PaymentServiceDep,
):
    return await payment_service.get_by_id(payment_id=payment_id)


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    payment_service: PaymentServiceDep,
    user_id: CurrentUserIdDep,
):
    return await payment_service.create(user_id=user_id, data=payment_data)


@router.post("/{payment_id}/pay", response_model=PaymentResponse)
async def pay_for_booking(
    payment_id: int,
    payment_service: PaymentServiceDep,
    user_id: CurrentUserIdDep,
    process_data: PaymentProcessRequest | None = None,
):
    card_number = process_data.card_number if process_data else None
    return await payment_service.process_payment(
        payment_id=payment_id,
        card_number=card_number,
    )
