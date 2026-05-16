from pydantic import BaseModel


class FriendshipSchema(BaseModel):
    user1_id: int
    user2_id: int