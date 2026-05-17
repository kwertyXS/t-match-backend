import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


import sys
import os

# путь к корню проекта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

os.environ.setdefault("PG_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("PG_USER", "test")
os.environ.setdefault("PG_PASS", "test")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")