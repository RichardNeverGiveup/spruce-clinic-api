from pydantic import BaseSettings


class Settings(BaseSettings): #正常的环境变量应该是全大写，这里用小写没关系是因为pydantic帮忙进行了转换
    db_hostname: str
    db_port: str
    db_password: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"

settings = Settings()