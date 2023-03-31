from datetime import datetime
from datetime import timedelta

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    expires_at: datetime
    access_token: str

    @classmethod
    def from_api(cls, token_type: str, expires_in: int, access_token: str) -> "Token":
        return cls(
            token_type=token_type,
            expires_at=datetime.now() + timedelta(milliseconds=expires_in),
            access_token=access_token,
        )

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at
