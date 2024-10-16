import os
from functools import lru_cache
from dotenv import load_dotenv

from .utils import assemble_database_url


load_dotenv()


class Config:
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    SUPERUSER_GROUP_NAME = os.getenv("SUPERUSER_GROUP_NAME")
    SUPERUSER_GROUP_ABBREVIATION = os.getenv("SUPERUSER_GROUP_ABBREVIATION")
    FIRST_SUPERUSER = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD = os.getenv("FIRST_SUPERUSER_PASSWORD")

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    DEFAULT_USER_PASSWORD = os.getenv("DEFAULT_USER_PASSWORD")

    CKEDITOR_PKG_TYPE = "standard"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI = assemble_database_url(
        "postgresql",
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB,
    )


class LocalConfig(Config):
    DEBUG = True
    TESTING = False


class StagingConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


CONFIGS = {
    "local": LocalConfig(),
    "staging": StagingConfig(),
    "testing": TestingConfig(),
    "production": ProductionConfig(),
}


@lru_cache
def get_config(environment: str):
    config = CONFIGS.get(environment, None)

    if config is None:
        raise ValueError(f"Cannot found config for environment {environment}")

    return config
