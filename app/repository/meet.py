from app.db.models import Meeting
from app.db.session import LocalSession
from app.schemas.meet import MeetingSchema
from app.validators.time import ensure_msk


async def add_meet(data: MeetingSchema) -> Meeting:
     async with LocalSession() as session:
        time_msk = await ensure_msk(data.ends_at)
        stmt = (
            Meeting(title = data.title,
                    description = data.description,
                    ends_at = time_msk,
                    created_by=data.created_by
            )
        )
        session.add(stmt)
        await session.commit()
        await session.refresh(stmt)
        return stmt