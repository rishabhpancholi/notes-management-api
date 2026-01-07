from pydantic_settings import (
    BaseSettings, 
    SettingsConfigDict
)

class Config(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    jwt_secret_key: str

    @property
    def postgres_uri(self)-> str:
        return f"""postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"""
    
    model_config = SettingsConfigDict(env_file=".env")

app_config = Config()