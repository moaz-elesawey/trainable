from functools import lru_cache


class Config:
    DEBUG = False
    TESTING = False
    SUPERUSER_GROUP_NAME = "Super Users"
    SUPERUSER_GROUP_ABBREVIATION = "SU"
    FIRST_SUPERUSER = "admin"
    FIRST_SUPERUSER_PASSWORD = "P@ssw0rd"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    CKEDITOR_PKG_TYPE = "standard"
    DEFAULT_USER_PASSWORD = "P@ssw0rd"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


# def assemble_database_url(
#     driver: str, user: str, password: str, host: str, port: int, database: str
# ) -> str:
#     """Assemble Database URL"""

#     conn_string = "{}://{}:{}@{}:{}/{}".format(
#         quote(driver),
#         quote(user),
#         quote(password),
#         quote(host),
#         port,
#         quote(database),
#     )

#     return conn_string


class LocalConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = "1biPkWkAcTOAYkCGhTCqNnn9HP0fXhpruezp4VXFeZmKVyMJmWciKILA4KpJHNTLEBfBkqXNblB75kC6g-FyMg"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class StagingConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = "1biPkWkAcTOAYkCGhTCqNnn9HP0fXhpruezp4VXFeZmKVyMJmWciKILA4KpJHNTLEBfBkqXNblB75kC6g-FyMg"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = "testing-secret-key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "1biPkWkAcTOAYkCGhTCqNnn9HP0fXhpruezp4VXFeZmKVyMJmWciKILA4KpJHNTLEBfBkqXNblB75kC6g-FyMg"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


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
