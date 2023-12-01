from logging import config as logging_config
from pathlib import Path

from dotenv import dotenv_values
from pydantic import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

config = dotenv_values(BASE_DIR / ".env")

dev = bool(int(config["DEV"]))
if dev:
    api_config = dotenv_values(BASE_DIR / "env/api/.env.dev")
    redis_config = dotenv_values(BASE_DIR / "env/redis/.env.dev")
    elastic_config = dotenv_values(BASE_DIR / "env/elasticsearch/.env.dev")
    docker_config = dotenv_values(BASE_DIR / "env/docker/.env.dev")
    postgres_config = dotenv_values(BASE_DIR / "env/postgres/.env.dev")
else:
    api_config = dotenv_values(BASE_DIR / "env/api/.env")
    redis_config = dotenv_values(BASE_DIR / "env/redis/.env")
    elastic_config = dotenv_values(BASE_DIR / "env/elasticsearch/.env")
    docker_config = dotenv_values(BASE_DIR / "env/docker/.env")
    postgres_config = dotenv_values(BASE_DIR / "env/postgres/.env")


class ProjectSettings(BaseSettings):
    project_name: str = api_config["PROJECT_NAME"]


class RedisSettings(BaseSettings):
    host: str = docker_config["REDIS_HOST"]
    port: str = redis_config["REDIS_PORT"]


class ElasticConfig(BaseSettings):
    host: str = docker_config["ELASTIC_HOST"]
    port: str = elastic_config["ELASTIC_PORT"]
    url: str = f"http://{host}:{port}"
    film_idx: str = elastic_config["ELASTIC_FILM_INDEX"]
    search_idx: str = elastic_config["ELASTIC_SEARCH_INDEX"]
    genre_idx: str = elastic_config["ELASTIC_GENRE_INDEX"]
    actor_idx: str = elastic_config["ELASTIC_ACTOR_INDEX"]
    writer_idx: str = elastic_config["ELASTIC_WRITER_INDEX"]
    director_idx: str = elastic_config["ELASTIC_DIRECTOR_INDEX"]
    scroll: str = "2s"
    scroll_size: int = 100


class Settings(BaseSettings):
    project: ProjectSettings = ProjectSettings()
    redis: RedisSettings = RedisSettings()
    elastic: ElasticConfig = ElasticConfig()
    cache_expire_in_seconds: int = 60 * 5
    dev_params: bool = dev
    default_page_size: int = 10
    default_page_number: int = 1
