import pandas as pd
from unidecode import unidecode

# ── Constants ─────────────────────────────────────────────────────────────
FALLBACK_LEAGUES = [
    "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"
]
POSITION_FALLBACK = ["GK", "DF", "MF", "FW"]

# ── Helpers: available-* lists ────────────────────────────────────────────
def available_leagues(df: pd.DataFrame) -> list[str]:
    leagues = sorted(df["competition"].dropna().unique()) if "competition" in df.columns else []
    return leagues or FALLBACK_LEAGUES

def available_teams(df: pd.DataFrame, league: str | None) -> list[str]:
    if league is None or league.lower().startswith("all"):
        teams = df["team"].dropna().unique()
    else:
        teams = df.loc[df["competition"] == league, "team"].dropna().unique()
    return sorted(teams)

def available_positions(df: pd.DataFrame) -> list[str]:
    pos = sorted(df["position"].dropna().unique()) if "position" in df.columns else []
    return pos or POSITION_FALLBACK

def available_roles(df: pd.DataFrame) -> list[str]:
    return sorted(df["role"].dropna().unique()) if "role" in df.columns else []

# ── Filters ───────────────────────────────────────────────────────────────
def filter_by_league(df, league):
    return df if league is None or str(league).lower().startswith("all") else df[df["competition"] == league]

def filter_by_team(df, teams):
    return df if not teams or "All teams" in teams else df[df["team"].isin(teams)]

def filter_by_position(df, positions):
    return df if not positions or "All positions" in positions else df[df["position"].isin(positions)]

def filter_by_role(df, roles):
    return df if not roles or "All roles" in roles else df[df["role"].isin(roles)]

def normalize(text: str) -> str:
    return unidecode(text).lower()

def filter_by_name(df, query: str | None):
    if not query or len(query) < 3:
        return df
    q = normalize(query)
    mask = df["player"].fillna("").apply(lambda x: q in normalize(x))
    return df[mask]

# ── Master helper ─────────────────────────────────────────────────────────
def apply_all_filters(df, league, teams, positions, roles, search_name):
    df1 = filter_by_league(df, league)
    df2 = filter_by_team(df1, teams)
    df3 = filter_by_position(df2, positions)
    df4 = filter_by_role(df3, roles)
    return filter_by_name(df4, search_name)
