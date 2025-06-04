# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER, TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CustomWorkbook(Base):
    __tablename__ = "custom_workbook"

    workbook_id: Mapped[str] = mapped_column(
        Uuid(as_uuid=False), primary_key=True, default=lambda _: str(uuid.uuid4())
    )

    user_id: Mapped[str] = mapped_column(Uuid(as_uuid=False))

    task_level: Mapped[str] = mapped_column(String(128))
    title: Mapped[str] = mapped_column(String(1024))
    prompt: Mapped[str] = mapped_column(String(1024))
    img_url: Mapped[str] = mapped_column(String(1024))
    essay: Mapped[str] = mapped_column(TEXT)
    min_words: Mapped[int] = mapped_column(INTEGER)
    labels: Mapped[list[str]] = mapped_column(ARRAY(String(512)))
