from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sshtunnel import SSHTunnelForwarder

from alembic import context
from config import settings
from db import Base
from ssh_tunnel_config import ssh_settings

# Initialize settings (singleton-like usage)

# Configure SSH tunnel
server = SSHTunnelForwarder(
    (ssh_settings.ip, ssh_settings.port),  # Remote server IP and SSH port
    ssh_username=ssh_settings.ssh_username,
    ssh_private_key=ssh_settings.ssh_private_key_location,
    remote_bind_address=ssh_settings.remote_bind_address,  # Database port on remote server
    local_bind_address=ssh_settings.local_bind_address,  # Local port for the tunnel
)

server.start()

# Update SQLAlchemy URL with the tunneled port
config = context.config
config.set_main_option(
    'sqlalchemy.url', settings.DATABASE_URL
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
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
