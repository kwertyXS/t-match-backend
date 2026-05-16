from app.schemas.friend import FriendshipSchema
from app.repository.friend import add_users_friendship, accept_friendship, deny_friend


async def add_friendship(data: FriendshipSchema):
    user1 = min(data.user1_id, data.user2_id)
    user2 = max(data.user2_id, data.user1_id)
    friendship = await add_users_friendship(user1, user2)
    return friendship

async def accept_friend(data: FriendshipSchema):
    user1 = min(data.user1_id, data.user2_id)
    user2 = max(data.user2_id, data.user1_id)
    friendship = await accept_friendship(user1, user2)
    return friendship

async def deny_friendship(data: FriendshipSchema):
    user1 = min(data.user1_id, data.user2_id)
    user2 = max(data.user2_id, data.user1_id)
    await deny_friend(user1, user2)
    return {"ok": True}