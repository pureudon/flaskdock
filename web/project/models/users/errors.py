


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserNotExistsError(Exception):
    pass


class IncorrectPasswordError(Exception):
    pass


class UserAlreadyRegisteredError(UserError):
    pass


class InvalidEmailError(UserError):
    pass