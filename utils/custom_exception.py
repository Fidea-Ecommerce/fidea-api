class UserNotSeller(Exception):
    def __init__(self, message="user not seller"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message="user not found"):
        self.message = message
        super().__init__(self.message)


class ProductFoundError(Exception):
    def __init__(self, message="product not found"):
        self.message = message
        super().__init__(self.message)


class ProductAlready(Exception):
    def __init__(self, message="product already at database"):
        self.message = message
        super().__init__(self.message)


class StockNotAvaible(Exception):
    def __init__(self, message="stock not avaible"):
        self.message = message
        super().__init__(self.message)


class NumberMoreThan0(Exception):
    def __init__(self, message="number must be greater than 0"):
        self.message = message
        super().__init__(self.message)


class ProductNotAvaible(Exception):
    def __init__(self, message="product not avaible"):
        self.message = message
        super().__init__(self.message)


class InvalidInput(Exception):
    def __init__(self, message="Input Not Valid"):
        self.message = message
        super().__init__(self.message)


class UsernameRequired(Exception):
    def __init__(self, message="username is required"):
        self.message = message
        super().__init__(self.message)


class EmailRequired(Exception):
    def __init__(self, message="email is required"):
        self.message = message
        super().__init__(self.message)


class PasswordRequired(Exception):
    def __init__(self, message="password is required"):
        self.message = message
        super().__init__(self.message)


class ConfirmPasswordRequired(Exception):
    def __init__(self, message="confirm password is required"):
        self.message = message
        super().__init__(self.message)


class PasswordRequired(Exception):
    def __init__(self, message="password is required"):
        self.message = message
        super().__init__(self.message)


class TokenRequired(Exception):
    def __init__(self, message="token is required"):
        self.message = message
        super().__init__(self.message)


class UserIsActive(Exception):
    def __init__(self, message="user is active"):
        self.message = message
        super().__init__(self.message)


class EmailNotValid(Exception):
    def __init__(self, message="email not valid"):
        self.message = message
        super().__init__(self.message)


class UserNotIsActive(Exception):
    def __init__(self, message="user not is active"):
        self.message = message
        super().__init__(self.message)
