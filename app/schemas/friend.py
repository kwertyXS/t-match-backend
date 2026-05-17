from pydantic import BaseModel


class FriendshipSchema(BaseModel):
    user_login: str
