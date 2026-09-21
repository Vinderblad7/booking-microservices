from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "64dd9b0a123a"
down_revision: Union[str, Sequence[str], None] = "ee4fdf21cef2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

booking_status_enum = postgresql.ENUM(
    "PENDING", "PAID", "CANCELLED", name="bookingstatus"
)


def upgrade() -> None:
    booking_status_enum.create(op.get_bind(), checkfirst=True)
    op.execute(
        "ALTER TABLE bookings ALTER COLUMN status TYPE bookingstatus USING status::bookingstatus"
    )
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )


def downgrade() -> None:
    op.alter_column(
        "bookings",
        "created_at",
        existing_type=sa.DateTime(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=False,
        existing_server_default=sa.text("now()"),
    )
    op.alter_column(
        "bookings",
        "status",
        existing_type=booking_status_enum,
        type_=sa.VARCHAR(length=9),
        existing_nullable=False,
    )
    booking_status_enum.drop(op.get_bind(), checkfirst=True)