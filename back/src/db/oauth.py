from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB

from db.connect import Base


class OAuthProvider(Base):
    __tablename__ = "oauth_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # e.g., Google, Facebook
    client_id = Column(String, nullable=False)
    client_secret = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"
    __table_args__ = (
        Index("ix_oauth_accounts_provider_user", "provider_id", "provider_user_id"),
    )
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    provider_id = Column(Integer, ForeignKey("oauth_providers.id"))
    provider_user_id = Column(String, index=True)  # ID provided by OAuth provider
    token_id = Column(String, nullable=True)  # token for request user data (used in vk)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RawExternalData(Base):
    __tablename__ = "raw_external_data"
    __table_args__ = (
        Index("ix_raw_external_data_provider_user", "provider_id", "provider_user_id"),
    )
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey("oauth_providers.id"))
    provider_user_id = Column(String)  # ID provided by OAuth provider
    data = Column(JSONB, nullable=True)
