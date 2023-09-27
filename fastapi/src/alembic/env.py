import sys
import os
from pathlib import Path

current_dir = str(Path(os.getcwd()).parent)
print(current_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)

from logging.config import fileConfig
from sqlalchemy import create_engine
from alembic import context
from src.models import base, users, files_requests
from src.core.settings import settings

config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = base.Base.metadata


def run_migrations_offline() -> None:
    url = settings.connection_string
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        settings.connection_string
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
