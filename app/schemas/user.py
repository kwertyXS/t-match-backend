from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    nickname: str
    email: str
    telegram: str

    @field_validator("email")
    def validate_email(cls, v) -> str:
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("Некорректный формат email")
        return v.lower()