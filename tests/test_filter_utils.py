import pandas as pd
from app.services.filter_utils import available_leagues, filter_by_league
from app.services.filter_utils import (
    available_leagues,
    filter_by_league,
    available_teams,
    filter_by_team,
    available_positions,
    available_roles,
    filter_by_position,
    filter_by_role,
)

from app.services.filter_utils import filter_by_name


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

def test_position_role_filters():
    df = pd.DataFrame({
        "position": ["GK", "DF", "DF", "MF"],
        "role": ["Sweeper", "CB", "LB", "CM"],
    })
    # available lists
    assert available_positions(df) == ["DF", "GK", "MF"]
    assert available_roles(df) == ["CB", "CM", "LB", "Sweeper"]

    # filtering
    out = filter_by_position(df, ["DF"])
    assert len(out) == 2 and out["position"].unique()[0] == "DF"

    out2 = filter_by_role(df, ["LB", "CM"])
    assert len(out2) == 2 and set(out2["role"]) == {"LB", "CM"}

def test_fuzzy_name_search():
    df = pd.DataFrame({
        "player": ["Álvaro Morata", "Erling Haaland", "Kylian Mbappé"],
        "metric": [1, 2, 3],
    })
    assert len(filter_by_name(df, "mora")) == 1          # case-insensitive
    assert len(filter_by_name(df, "Haá")) == 1           # accent & substr
    assert len(filter_by_name(df, "xy")) == len(df)      # <3 chars → no filter