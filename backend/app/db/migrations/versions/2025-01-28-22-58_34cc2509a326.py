"""empty message.

Revision ID: 34cc2509a326
Revises: 819cbf6e030b
Create Date: 2025-01-28 22:58:03.423207

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "34cc2509a326"
down_revision = "819cbf6e030b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Run the migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "weather_data",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Float(), nullable=False),
        sa.Column("pressure", sa.Float(), nullable=False),
        sa.Column("wind_speed", sa.Float(), nullable=True),
        sa.Column("wind_direction", sa.String(length=50), nullable=True),
        sa.Column("precipitation_type", sa.String(length=50), nullable=True),
        sa.Column("precipitation_intensity", sa.Float(), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_weather_data_id"), "weather_data", ["id"], unique=False)
    op.create_index(
        op.f("ix_weather_data_timestamp"),
        "weather_data",
        ["timestamp"],
        unique=False,
    )
    op.create_table(
        "weather_forecast",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("forecast_time", sa.DateTime(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=True),
        sa.Column("humidity", sa.Float(), nullable=True),
        sa.Column("pressure", sa.Float(), nullable=True),
        sa.Column("wind_speed", sa.Float(), nullable=True),
        sa.Column("wind_direction", sa.String(length=50), nullable=True),
        sa.Column("precipitation_type", sa.String(length=50), nullable=True),
        sa.Column("precipitation_intensity", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_weather_forecast_created_at"),
        "weather_forecast",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_weather_forecast_forecast_time"),
        "weather_forecast",
        ["forecast_time"],
        unique=False,
    )
    op.create_index(
        op.f("ix_weather_forecast_id"),
        "weather_forecast",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Undo the migration."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_weather_forecast_id"), table_name="weather_forecast")
    op.drop_index(
        op.f("ix_weather_forecast_forecast_time"),
        table_name="weather_forecast",
    )
    op.drop_index(op.f("ix_weather_forecast_created_at"), table_name="weather_forecast")
    op.drop_table("weather_forecast")
    op.drop_index(op.f("ix_weather_data_timestamp"), table_name="weather_data")
    op.drop_index(op.f("ix_weather_data_id"), table_name="weather_data")
    op.drop_table("weather_data")
    # ### end Alembic commands ###
