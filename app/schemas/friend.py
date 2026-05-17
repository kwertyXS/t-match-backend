from pydantic import BaseModel


class FriendshipSchema(BaseModel):
    user_login: str


class FriendshipAnswerSchema(BaseModel):
    id: int
    user_id: int
    friend_id: int