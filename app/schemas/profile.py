from typing import List

from pydantic import BaseModel, field_validator


class ProfileCreateSchema(BaseModel):
    title: str
    description: str = None
    tags: List[str]

    @field_validator("title")
    def title_validator(cls, title):
        if len(title) > 30:
            raise ValueError("Title too long")
        if len(title) < 3:
            raise ValueError("Title too short")
        return title


class ProfileUpdateSchema(ProfileCreateSchema):
    id: int


class ResponseProfileSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    tags: List[str]
