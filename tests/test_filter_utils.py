import pandas as pd
from app.services.filter_utils import available_leagues, filter_by_league
from app.services.filter_utils import available_teams, filter_by_team


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

def test_available_teams_cascades():
    data = {
        "competition": ["EPL", "EPL", "La Liga"],
        "team": ["Arsenal", "Chelsea", "Barça"],
    }
    df = pd.DataFrame(data)
    assert available_teams(df, "EPL") == ["Arsenal", "Chelsea"]
    assert available_teams(df, "All") == ["Arsenal", "Barça", "Chelsea"]

def test_filter_by_team_multi():
    data = {"team": ["A", "B", "C"], "metric": [1, 2, 3]}
    df = pd.DataFrame(data)
    sub = filter_by_team(df, ["A", "C"])
    assert len(sub) == 2 and set(sub["team"]) == {"A", "C"}