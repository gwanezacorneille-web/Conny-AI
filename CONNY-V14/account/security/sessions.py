from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import secrets


@dataclass
class Session:
    token: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    active: bool = True


class SessionManager:

    def __init__(self, lifetime_hours=24):
        self.lifetime = timedelta(hours=lifetime_hours)
        self.sessions = {}

    def create(self, user_id):
        now = datetime.now(timezone.utc)

        session = Session(
            token=secrets.token_urlsafe(48),
            user_id=user_id,
            created_at=now,
            expires_at=now + self.lifetime,
        )

        self.sessions[session.token] = session

        return session

    def validate(self, token):
        session = self.sessions.get(token)

        if session is None:
            return None

        if not session.active:
            return None

        if datetime.now(timezone.utc) >= session.expires_at:
            session.active = False
            return None

        return session

    def revoke(self, token):
        session = self.sessions.get(token)

        if session is None:
            return False

        session.active = False
        return True
