from app.db.models import Profile
from app.db.session import LocalSession
from app.schemas.profile import ProfileSchema


async def add_profile(data: ProfileSchema, user_id: int) -> Profile:
     async with LocalSession() as session:
        stmt = (
            Profile(user_id = user_id,
                    title = data.title,
                    description = data.description,
                    tags = data.tags
            )
        )
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt