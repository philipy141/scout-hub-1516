import pandas as pd
from app.services.filter_utils import available_leagues, filter_by_league

def test_filter_returns_subset():
    data = {
        "competition": ["Premier League", "La Liga", "Premier League"],
        "player": ["A", "B", "C"],
    }
    df = pd.DataFrame(data)
    leagues = available_leagues(df)
    assert "Premier League" in leagues

    sub = filter_by_league(df, "Premier League")
    assert len(sub) == 2
    assert all(sub["competition"] == "Premier League")

def test_filter_all_returns_original():
    df = pd.DataFrame({"competition": ["X"], "player": ["P"]})
    out = filter_by_league(df, "All")
    assert len(out) == 1
