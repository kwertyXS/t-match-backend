from pydantic import BaseModel, field_validator



class RegistrationSchema(BaseModel):
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

class LoginSchema(RegistrationSchema):
    pass


