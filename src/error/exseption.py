class BaseCustomException(Exception):
    default_message = None

    def __init__(self, message: str | None = None, *args, **kwargs) -> None:
        msg = message or self.default_message
        super().__init__(msg, *args, **kwargs)


class UserError(BaseCustomException):
    default_message = "Пользователь не найден"


class AccountError(BaseCustomException):
    default_message = "Аккаунт не найден"


class ToManySessions(AccountError):
    default_message = "Превышено количество сессий, максимум 5"
