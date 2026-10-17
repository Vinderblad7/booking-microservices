from decimal import Decimal

from app.exceptions import (
    PaymentAlreadyExistsError,
    PaymentAlreadyProcessedError,
    PaymentNotFoundError,
)
from app.models.payment import Payment, PaymentStatus
from app.repositories.payment import PaymentRepository
from app.schemas.payment import PaymentCreate
from app.services.gateway import MockPaymentGateway


class PaymentService:
    def __init__(
        self,
        payment_repo: PaymentRepository,
        gateway: MockPaymentGateway | None = None,
    ):
        self.payment_repo = payment_repo
        self.gateway = gateway or MockPaymentGateway()

    async def get_all(
        self,
        user_id: int | None = None,
        booking_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Payment]:
        return await self.payment_repo.get_all(
            user_id=user_id,
            booking_id=booking_id,
            skip=skip,
            limit=limit,
        )

    async def get_by_id(self, payment_id: int) -> Payment:
        payment = await self.payment_repo.get_by_id(payment_id)
        if not payment:
            raise PaymentNotFoundError(f"Payment with id {payment_id} not found")
        return payment

    async def get_by_booking_id(self, booking_id: int) -> Payment:
        payment = await self.payment_repo.get_by_booking_id(booking_id)
        if not payment:
            raise PaymentNotFoundError(f"Payment for booking id {booking_id} not found")
        return payment

    async def create(self, user_id: int, data: PaymentCreate) -> Payment:
        existing = await self.payment_repo.get_by_booking_id(data.booking_id)
        if existing and existing.status == PaymentStatus.SUCCESS:
            raise PaymentAlreadyExistsError(
                f"Payment for booking id {data.booking_id} already completed"
            )
        if existing and existing.status == PaymentStatus.PENDING:
            return existing

        payment_data = data.model_dump()
        payment_data["user_id"] = user_id
        payment_data["status"] = PaymentStatus.PENDING

        return await self.payment_repo.create(payment_data)

    async def process_payment(
        self, payment_id: int, card_number: str | None = None
    ) -> Payment:
        payment = await self.get_by_id(payment_id)
        if payment.status == PaymentStatus.SUCCESS:
            raise PaymentAlreadyProcessedError("Payment has already been processed")

        is_success = await self.gateway.process_payment(
            amount=payment.amount, card_number=card_number
        )
        new_status = PaymentStatus.SUCCESS if is_success else PaymentStatus.FAILED

        return await self.payment_repo.update(payment, {"status": new_status})
