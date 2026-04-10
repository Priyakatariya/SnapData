import os
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv
from typing import Any

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "")

connect_args = {"check_same_thread": False} if DATABASE_URL and DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args) if DATABASE_URL else None


def get_schema_string() -> str:
    """Returns DB schema as a human-readable string for the Gemini prompt."""
    if not engine:
        return "No database connected."

    inspector = inspect(engine)
    lines = []
    for table_name in inspector.get_table_names():
        cols = inspector.get_columns(table_name)
        col_defs = ", ".join(
            f"{c['name']} ({str(c['type'])})" for c in cols
        )
        lines.append(f"Table: {table_name} | Columns: {col_defs}")
    return "\n".join(lines)


def get_schema_metadata() -> list[dict]:
    """Returns structured schema metadata for the /api/schema endpoint."""
    if not engine:
        return []

    inspector = inspect(engine)
    tables = []
    for table_name in inspector.get_table_names():
        cols = inspector.get_columns(table_name)
        tables.append({
            "table_name": table_name,
            "columns": [
                {
                    "name": c["name"],
                    "type": str(c["type"]),
                    "nullable": c.get("nullable", True),
                }
                for c in cols
            ],
        })
    return tables


def execute_query(sql: str) -> tuple[list[str], list[dict[str, Any]]]:
    """
    Executes a SELECT SQL query and returns (columns, rows).
    Raises ValueError for non-SELECT statements.
    """
    stripped = sql.strip().lower()
    if not stripped.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    if not engine:
        raise RuntimeError("No database connection configured.")

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        columns = list(result.keys())
        rows = [dict(zip(columns, row)) for row in result.fetchall()]
    return columns, rows
