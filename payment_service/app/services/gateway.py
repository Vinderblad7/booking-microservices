import asyncio
from decimal import Decimal


class MockPaymentGateway:
    async def process_payment(
        self, amount: Decimal, card_number: str | None = None
    ) -> bool:
        await asyncio.sleep(0.5)
        if card_number and card_number.endswith("0000"):
            return False
        return True
