"""Database configuration and initialization."""

import os
from typing import Optional, Union

from agno.db.sqlite import SqliteDb
from agno.db.postgres import PostgresDb

def get_db(db_file: str = "data/brandforge.db", session_table: str = "agent_sessions") -> SqliteDb:
    """Get a configured SqliteDb instance."""
    return SqliteDb(
        session_table=session_table,
        db_file=db_file,
    )

def get_postgres_db(database_url: Optional[str] = None, session_table: str = "agent_sessions") -> Optional[PostgresDb]:
    """Get a PostgresDb instance for production if URL is provided."""
    url = database_url or os.environ.get("DATABASE_URL")
    if url:
        return PostgresDb(
            session_table=session_table,
            db_url=url,
        )
    return None

def init_database() -> None:
    """Initialize database and create tables/storage."""
    os.makedirs("data", exist_ok=True)
    db = get_db()
    # AGNO v3 manages schema initialization internally, no need to call .create()

