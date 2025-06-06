import streamlit as st
from services.data_loader import load_players_df
from services.filter_utils import (
    available_leagues,
    filter_by_league,
    available_teams,
    filter_by_team,
)

st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")

df = load_players_df()
st.success(f"Loaded {len(df):,} player rows")
st.info("🚧 Feature work in progress. Use the sidebar to navigate.")

# ── Sidebar: League selector ───────────────────────────────────────────────
st.sidebar.header("Filters")

all_league_label = f"All ({len(df):,} players)"
league = st.sidebar.selectbox(
    "League",
    [all_league_label] + available_leagues(df),
    index=0,
)

df_league = filter_by_league(df, league)

# ── Sidebar: Team multi-select (cascades) ──────────────────────────────────
team_list = available_teams(df_league, league)
all_team_label = "All teams"
teams_selected = st.sidebar.multiselect(
    "Team (multi-select)",
    [all_team_label] + team_list,
    default=all_team_label,
)

df = filter_by_team(df_league, teams_selected)

# ── Main body ──────────────────────────────────────────────────────────────
st.success(f"Loaded {len(df):,} player rows")
st.dataframe(df.head(50), use_container_width=True)
