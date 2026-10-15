# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
# Импортируем асинхронный метод создания движка
from sqlalchemy.ext.asyncio import async_engine_from_config 

from alembic import context

# Твои кастомные импорты приложения
from config import settings
from database import Base
import models  # Нам нужны модели, чтобы Base.metadata наполнился таблицами

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные наших моделей для автогенерации
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.database_url
    
    # Корректируем схему для офлайн-режима
    if url.startswith("sqlite://") and not url.startswith("sqlite+aiosqlite://"):
        url = url.replace("sqlite://", "sqlite+aiosqlite://")
    elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ВОТ ЭТА ФУНКЦИЯ БЫЛА УТЕРЯНА — возвращаем её на место
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    
    # Автоматически корректируем протокол для Postgres/SQLite под асинхронность
    url = settings.database_url
    if url.startswith("sqlite://") and not url.startswith("sqlite+aiosqlite://"):
        url = url.replace("sqlite://", "sqlite+aiosqlite://")
    elif url.startswith("postgresql://") and not url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://")
        
    configuration["sqlalchemy.url"] = url

    # Создаем асинхронный движок
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Асинхронное подключение
    async with connectable.connect() as connection:
        # Выполняем миграции
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Запускаем асиннадцатый цикл для миграций
    asyncio.run(run_migrations_online())