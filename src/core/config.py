from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "local"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    HASH_SALT: str = ":)"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def SYNC_DATABASE_URL(self):
        return (
            f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


app_config = Config()
