from app.config.base_settings import Settings


class DBConfig(Settings):
    database_url: str


db_config = DBConfig()
