from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    app_description: str = 'Все на переговоры!'
    app_version: str = '1.0.0'

    class Config:
        env_file = '.env'


settings = Settings()
