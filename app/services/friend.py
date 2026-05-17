from fastapi import Depends, HTTPException

from app.repository.user import get_user_by_login
from app.schemas.friend import FriendshipSchema
from app.repository.friend import add_users_friendship, accept_friendship, deny_friend, is_friendship_exists, \
    get_friends
from app.validators.password import get_current_user


async def add_friendship(data: FriendshipSchema, current_user: dict = Depends(get_current_user)):
    user_1 = await get_user_by_login(current_user['login'])
    user_2 = await get_user_by_login(data.user_login)
    if not user_1 or not user_2:
        raise HTTPException(status_code=404, detail="User not found")
    if user_1.id == user_2.id:
        raise HTTPException(status_code=403, detail="User can't be same")
    user1 = min(user_1.id, user_2.id)
    user2 = max(user_1.id, user_2.id)
    is_friendship = await is_friendship_exists(user1, user2)
    if is_friendship:
        raise HTTPException(status_code=400, detail="Friendship already exists")
    friendship = await add_users_friendship(user1, user2)
    return friendship

async def accept_friend(data: FriendshipSchema, current_user: dict = Depends(get_current_user)):
    user_1 = await get_user_by_login(current_user['login'])
    user_2 = await get_user_by_login(data.user_login)
    if not user_1 or not user_2:
        raise HTTPException(status_code=404, detail="User not found")
    user1 = min(user_1.id, user_2.id)
    user2 = max(user_1.id, user_2.id)
    friendship = await accept_friendship(user1, user2)
    return friendship

async def deny_friendship(data: FriendshipSchema, current_user: dict = Depends(get_current_user)):
    user_1 = await get_user_by_login(current_user['login'])
    user_2 = await get_user_by_login(data.user_login)
    if not user_1 or not user_2:
        raise HTTPException(status_code=404, detail="User not found")
    user1 = min(user_1.id, user_2.id)
    user2 = max(user_1.id, user_2.id)
    await deny_friend(user1, user2)
    return {"ok": True}

async def get_user_friends(current_user: dict = Depends(get_current_user)):
    user = await get_user_by_login(current_user['login'])
    friends = await get_friends(user.id)
    print("USERS FRIENDS", friends)
    return friends