import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")
TEST_DATABASE_URI = os.environ.get(
    "TEST_DATABASE_URI",
    f"postgresql+asyncpg://{DB_USER_TEST}:"
    f"{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}",
)

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DATABASE_URI = os.environ.get(
    "DATABASE_URI",
    f"postgresql+asyncpg://"
    f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)


@dataclass(frozen=True)
class DatabaseConfig:
    db_uri: str

    @staticmethod
    def from_env() -> "DatabaseConfig":
        uri = os.getenv("DATABASE_URI", DATABASE_URI)

        if not uri:
            raise RuntimeError("Missing DATABASE_URI environment variable")

        return DatabaseConfig(uri)


REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}"


@dataclass(frozen=True)
class RedisConfig:
    rd_uri: str

    @staticmethod
    def from_env() -> "RedisConfig":
        uri = os.environ.get("REDIS_URI", REDIS_URI)

        if not uri:
            raise RuntimeError("Missing REDIS_URI environment variable")

        return RedisConfig(uri)


DB_HOST_TEST = os.environ.get("DB_HOST_TEST")
DB_PORT_TEST = os.environ.get("DB_PORT_TEST")
DB_NAME_TEST = os.environ.get("DB_NAME_TEST")
DB_USER_TEST = os.environ.get("DB_USER_TEST")
DB_PASS_TEST = os.environ.get("DB_PASS_TEST")

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

API_ADMIN_PWD = os.environ.get("API_ADMIN_PWD")


class MinIOConfig(BaseModel):
    endpoint_url: str = os.getenv("MINIO_ENDPOINT_URL")
    access_key: str = os.getenv("MINIO_ACCESS_KEY")
    secret_key: str = os.getenv("MINIO_SECRET_KEY")


@dataclass(frozen=True)
class FirebaseConfig:
    rd_uri: str

    @staticmethod
    def from_env() -> "FirebaseConfig":
        uri = os.getenv("FIREBASE_CONFIG_PATH", None)

        if not uri:
            raise RuntimeError("Missing FIREBASE_CONFIG_PATH environment variable")

        return FirebaseConfig(uri)
