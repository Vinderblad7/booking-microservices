class PaymentNotFoundError(Exception):
    def __init__(self, message: str = "Payment not found"):
        self.message = message
        super().__init__(self.message)


class PaymentAlreadyExistsError(Exception):
    def __init__(self, message: str = "Payment for this booking already exists"):
        self.message = message
        super().__init__(self.message)


class PaymentAlreadyProcessedError(Exception):
    def __init__(self, message: str = "Payment has already been processed"):
        self.message = message
        super().__init__(self.message)


class PaymentFailedError(Exception):
    def __init__(self, message: str = "Payment processing failed"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(Exception):
    def __init__(self, message: str = "Invalid or expired token"):
        self.message = message
        super().__init__(self.message)
