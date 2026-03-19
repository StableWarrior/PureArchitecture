import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from .connection import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id = Column(String, nullable=False)
    item_id = Column(UUID(as_uuid=True), nullable=False)

    quantity = Column(Integer, nullable=False, default=1)

    status = Column(String, nullable=False, default="NEW")

    idempotency_key = Column(UUID(as_uuid=True), nullable=False, unique=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Vladivostok")),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Vladivostok")),
        onupdate=lambda: datetime.now(ZoneInfo("Asia/Vladivostok")),
    )
