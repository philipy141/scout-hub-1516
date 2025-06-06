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
