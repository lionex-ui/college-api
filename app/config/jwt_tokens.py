from app.config.base_settings import Settings


class JWTConfig(Settings):
    secret: str
    access_token_lifetime_minutes: int
    refresh_token_lifetime_days: int


jwt_config = JWTConfig()
