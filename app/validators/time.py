import datetime
from zoneinfo import ZoneInfo

MOSCOW_TZ = ZoneInfo("Europe/Moscow")  # UTC+3

async def ensure_msk(dt: datetime.datetime) -> datetime.datetime:
    """Гарантирует, что datetime будет в МСК и будет timezone-aware."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # Если время без таймзоны, предполагаем, что оно уже в МСК
        dt = dt.replace(tzinfo=MOSCOW_TZ)
    else:
        # Конвертируем любую таймзону в МСК
        dt = dt.astimezone(MOSCOW_TZ)
    return dt