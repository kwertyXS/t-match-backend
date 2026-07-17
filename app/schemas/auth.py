from pydantic import BaseModel, field_validator, model_validator


class LoginSchema(BaseModel):
    login: str
    password: str

    @field_validator("login")
    def login_validator(cls, login):
        login = login.strip()
        if len(login) < 6 or len(login) > 30:
            raise ValueError("Invalid login")
        return login

    @field_validator("password")
    def password_validator(cls, password):
        password = password.strip()
        if len(password) < 5 or len(password) > 30:
            raise ValueError("Invalid password")
        return password


class RegistrationSchema(LoginSchema):
    email: str | None = None
    telegram: str | None = None

    @model_validator(mode="after")
    def validate_email_or_telegram(self):
        if not self.email and not self.telegram:
            raise ValueError("Email or Telegram required")
        return self

    @field_validator("email")
    def validate_email(cls, email) -> str:
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Некорректный формат email")
        return email.lower()


class AccessTokenAnswerSchema(BaseModel):
    access_token: str


class RefreshTokenAnswerSchema(BaseModel):
    refresh_token: str
