import pandas as pd

# -------- config --------
FALLBACK_LEAGUES = [
    "Premier League",        # England
    "La Liga",               # Spain
    "Serie A",               # Italy
    "Bundesliga",            # Germany
    "Ligue 1",               # France
]

def available_leagues(df: pd.DataFrame) -> list[str]:
    """Return sorted list of league names present in the DataFrame.
    Falls back to pre-defined list if column missing or empty."""
    if "competition" in df.columns:
        leagues = sorted(df["competition"].dropna().unique())
        if leagues:
            return leagues
    return FALLBACK_LEAGUES

def filter_by_league(df: pd.DataFrame, league: str | None) -> pd.DataFrame:
    """Return df filtered by league; None or 'All' returns original df."""
    if league is None or league.lower().startswith("all"):
        return df
    if "competition" not in df.columns:
        return df  # nothing to filter on
    return df[df["competition"] == league]


def available_teams(df: pd.DataFrame, league: str | None) -> list[str]:
    """Return sorted list of teams for the chosen league."""
    if league is None or league.lower().startswith("all"):
        teams = df["team"].dropna().unique()
    else:
        teams = df.loc[df["competition"] == league, "team"].dropna().unique()
    return sorted(teams)


def filter_by_team(df: pd.DataFrame, teams: list[str] | None) -> pd.DataFrame:
    """Filter DataFrame by team(s). Empty / None returns original df."""
    if not teams or "All teams" in teams:
        return df
    return df[df["team"].isin(teams)]