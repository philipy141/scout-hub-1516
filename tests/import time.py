import time
import pytest
from app.services.data_loader import load_players_df, DBConnectionError

def test_load_under_two_seconds():
    start = time.time()
    df = load_players_df(force=True)
    elapsed = time.time() - start
    assert elapsed < 2.0, f"Load took {elapsed:.2f}s"
    assert not df.empty

def test_missing_db(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_URL", f"sqlite:///{tmp_path/'missing.db'}")
    with pytest.raises(DBConnectionError):
        load_players_df(force=True)
