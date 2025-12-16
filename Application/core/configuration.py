from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):  # Класс настроек для подключения к бд

    user: str
    password: str
    host: str
    port: str
    db: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )  # Подгрузка параметров для подключения

    def ASYNC_ENGINE_CREATE(self):  # Создание ссылки на подключение к базе
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


settings = Settings()
