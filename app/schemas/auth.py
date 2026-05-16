from pydantic import BaseModel, field_validator

class LoginSchema(BaseModel):
    login: str
    password: str

class RegistrationSchema(LoginSchema):
    email: str = None
    telegram: str = None

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

    @field_validator("email")
    def validate_email(cls, email) -> str:
        if "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Некорректный формат email")
        return email.lower()



