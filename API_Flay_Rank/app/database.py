import os
from pathlib import Path

import psycopg
import redis
from dotenv import load_dotenv
from psycopg.rows import dict_row


ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

def connect() -> psycopg.Connection:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return psycopg.connect(database_url, row_factory=dict_row)


def init_db() -> None:
    connection = connect()
    connection.close()

def ping_redis() -> str:
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise RuntimeError("REDIS_URL is not set")
    client = redis.from_url(redis_url)
    try:
        if not client.ping():
            raise RuntimeError("Redis ping failed")
        return "PONG"
    finally:
        client.close()
