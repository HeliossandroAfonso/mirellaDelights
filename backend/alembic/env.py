import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- 1. IMPORTAÇÕES PARA O SEU PROJETO ---
from dotenv import load_dotenv
import sys

# Garante que o Python encontre a pasta 'app'
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.database import Base
from app.models.usuario import Usuario
from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.itemPedido import ItemPedido

# Carrega as variáveis do .env
load_dotenv()
# -----------------------------------------

config = context.config

# --- 2. CONFIGURA A URL DINAMICAMENTE ---
# Isso substitui o "driver://..." do alembic.ini pela sua URL real
section = config.config_ini_section
config.set_section_option(section, "sqlalchemy.url", os.getenv("DATABASE_URL"))
# -----------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- 3. VINCULA SEUS MODELOS ---
target_metadata = Base.metadata 
# -------------------------------

def run_migrations_offline() -> None:
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
    # Usa a configuração que alteramos acima com o DATABASE_URL
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