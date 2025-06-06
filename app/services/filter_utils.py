import pandas as pd
from unidecode import unidecode


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

    # ─────────────────── POSITION + ROLE HELPERS ───────────────────────────────
POSITION_FALLBACK = ["GK", "DF", "MF", "FW"]

def available_positions(df: pd.DataFrame) -> list[str]:
    """Return unique positions present; fallback to default list."""
    if "position" in df.columns:
        pos = sorted(df["position"].dropna().unique())
        if pos:
            return pos
    return POSITION_FALLBACK

def available_roles(df: pd.DataFrame) -> list[str]:
    """Return unique roles present."""
    if "role" in df.columns:
        return sorted(df["role"].dropna().unique())
    return []

def filter_by_position(df: pd.DataFrame, positions: list[str] | None) -> pd.DataFrame:
    if not positions or "All positions" in positions:
        return df
    return df[df["position"].isin(positions)]

def filter_by_role(df: pd.DataFrame, roles: list[str] | None) -> pd.DataFrame:
    if not roles or "All roles" in roles:
        return df
    return df[df["role"].isin(roles)]


# ─────────────────── NAME SEARCH HELPER ────────────────────────────────────
def normalize(text: str) -> str:
    """Lower-case and strip accents for robust comparison."""
    return unidecode(text).lower()

def filter_by_name(df: pd.DataFrame, query: str | None) -> pd.DataFrame:
    """Return subset whose player name contains the query (accent + case insensitive)."""
    if not query or len(query) < 3:
        return df
    q = normalize(query)
    mask = df["player"].fillna("").apply(lambda x: q in normalize(x))
    return df[mask]