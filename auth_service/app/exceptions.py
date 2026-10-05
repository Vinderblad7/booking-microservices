class UserNotFoundError(Exception):
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = "User with this email already exists"):
        self.message = message
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid email or password"):
        self.message = message
        super().__init__(self.message)


class UserInactiveError(Exception):
    def __init__(self, message: str = "User account is inactive"):
        self.message = message
        super().__init__(self.message)


class InvalidTokenError(Exception):
    def __init__(self, message: str = "Invalid or expired token"):
        self.message = message
        super().__init__(self.message)


class InsufficientPermissionsError(Exception):
    def __init__(self, message: str = "You do not have permission to perform this action"):
        self.message = message
        super().__init__(self.message)
