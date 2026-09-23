class HotelNotFoundError(Exception):
    def __init__(self, message: str = "Hotel not found"):
        self.message = message
        super().__init__(self.message)


class HotelAlreadyExistsError(Exception):
    def __init__(self, message: str = "Hotel already exists"):
        self.message = message
        super().__init__(self.message)


class RoomNotFoundError(Exception):
    def __init__(self, message: str = "Room not found"):
        self.message = message
        super().__init__(self.message)


class RoomNotAvailableError(Exception):
    def __init__(self, message: str = "Room is not available for selected dates"):
        self.message = message
        super().__init__(self.message)


class BookingNotFoundError(Exception):
    def __init__(self, message: str = "Booking not found"):
        self.message = message
        super().__init__(self.message)