import datetime
import random
import string

import jwt
from jwt import exceptions as jwt_exc

from app.config import jwt_config
from app.schemas import RefreshTokensRequest


class JWT:
    def __init__(self):
        self.secret = jwt_config.secret

    def _generate_access_token(self, username: str, is_main_administrator: bool) -> str:
        payload = {
            "username": username,
            "is_main_administrator": is_main_administrator,
            "exp": datetime.datetime.now(tz=datetime.UTC)
            + datetime.timedelta(minutes=jwt_config.access_token_lifetime_minutes),
        }

        return jwt.encode(payload, self.secret, algorithm="HS256")

    def _generate_refresh_token(self, username: str, is_main_administrator: bool, refresh_string: str) -> str:
        payload = {
            "refresh_string": refresh_string,
            "username": username,
            "is_main_administrator": is_main_administrator,
            "exp": datetime.datetime.now(tz=datetime.UTC)
            + datetime.timedelta(days=jwt_config.refresh_token_lifetime_days),
        }

        return jwt.encode(payload, self.secret, algorithm="HS256")

    def generate_token(self, username: str, is_main_administrator: bool) -> tuple[str, str, str]:
        refresh_string = "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=64))

        access_token = self._generate_access_token(username, is_main_administrator)
        refresh_token = self._generate_refresh_token(username, is_main_administrator, refresh_string)

        return access_token, refresh_token, refresh_string

    def verify_token(self, token: str) -> tuple[int, dict | None]:
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return 200, payload
        except (jwt_exc.ExpiredSignatureError, jwt_exc.InvalidTokenError):
            return 401, None

    def refresh_tokens(self, tokens: RefreshTokensRequest) -> tuple[int, str | None, str | None, str | None]:
        access_status_code, access_payload = self.verify_token(tokens.access_token)
        if access_status_code == 200:
            return 400, None, None, None

        refresh_status_code, refresh_payload = self.verify_token(tokens.refresh_token)
        if refresh_status_code == 401:
            return 401, None, None, None

        access_token, refresh_token, refresh_string = self.generate_token(
            refresh_payload["username"], refresh_payload["is_main_administrator"]
        )
        return 200, access_token, refresh_token, refresh_string
