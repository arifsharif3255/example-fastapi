
# pylint: disable=unused-import
# pylint: disable=missing-module-docstring
# pylint: disable=E0611
# pylint: disable=W0622
# pylint: disable=W0613
# pylint: disable=C0115


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION_MINUTE: int

    class Config:
                env_file= ".env"


settings = Settings()