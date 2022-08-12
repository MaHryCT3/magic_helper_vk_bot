import os

import peewee

from app.exceptions import FailedToDatabaseConnection


class BaseModel(peewee.Model):
    """A base database model."""

    class Meta:
        database = peewee.PostgresqlDatabase(
            host=os.getenv("DATABASE_HOST", "localhost"),
            port=os.getenv("DATABASE_PORT", "5432"),
            user=os.getenv("DATABASE_USER", "postgres"),
            password=os.getenv("DATABASE_PASSWORD", "postgres"),
            database=os.getenv("DATABASE_NAME", "postgres"),
        )

        try:
            database.connect()
        except peewee.OperationalError:
            raise FailedToDatabaseConnection
        finally:
            database.close()


class CheckModel(BaseModel):
    """Represents a check model."""

    id = peewee.AutoField()
    steamid = peewee.BigIntegerField(null=False)
    moder_vk = peewee.BigIntegerField(null=False)
    start_time = peewee.DateTimeField(null=False)
    end_time = peewee.DateTimeField(null=True)
    server_number = peewee.IntegerField(null=True)
    is_ban = peewee.BooleanField(null=False, default=False)

    class Meta:
        table_name = "Checks"
