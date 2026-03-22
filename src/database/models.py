import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

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

    idempotency_key = Column(String, nullable=False, unique=True)

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

    outbox = relationship(
        "Outbox",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    event_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)

    status = Column(String(50), nullable=False, index=True)  # pending / sent

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Vladivostok")),
    )

    order = relationship(
        "Order",
        back_populates="outbox",
    )


class Inbox(Base):
    __tablename__ = "inbox"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    event_type = Column(String, nullable=False)

    payload = Column(JSONB, nullable=False)

    status = Column(String(50), nullable=False, index=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Vladivostok")),
    )