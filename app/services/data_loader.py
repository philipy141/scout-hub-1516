import os
import sqlite3
import pandas as pd
from typing import Optional

CACHE: dict[str, pd.DataFrame] = {}

class DBConnectionError(RuntimeError):
    """Raised when the SQLite file is missing or unreadable."""

def get_db_path() -> str:
    """Resolve DB path from env var or default location."""
    db_url = os.environ.get("DB_URL", "sqlite:///data/players.db")
    if not db_url.startswith("sqlite:///"):
        raise ValueError("Only sqlite URLs are supported")
    path = db_url.replace("sqlite:///", "", 1)
    if not os.path.isfile(path):
        raise DBConnectionError(f"SQLite file not found at {path}")
    return path

def load_players_df(force: bool = False) -> pd.DataFrame:
    """
    Load entire players table into a pandas DataFrame.

    Caches result in-memory for reload speed.
    """
    if not force and "players" in CACHE:
        return CACHE["players"]

    path = get_db_path()
    conn = sqlite3.connect(path)
    df = pd.read_sql("SELECT * FROM big_five_leagues_1415_df", conn)  # table name = players
    conn.close()

    # Column typing
    numeric_cols = df.select_dtypes(include="float").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)

    CACHE["players"] = df
    return df
