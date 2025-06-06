import streamlit as st
from services.data_loader import load_players_df
from services.filter_utils import (
    available_leagues, filter_by_league,
    available_teams,   filter_by_team,
    available_positions, filter_by_position,
    available_roles,     filter_by_role,
    filter_by_name,
)

st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")

df_all = load_players_df(force=True)
st.success(f"Loaded {len(df_all):,} player rows")
st.info("🚧 Feature work in progress. Use the sidebar to navigate.")

# ── Sidebar: League filter ──────────────────────────────────────────────
st.sidebar.header("Filters")
league = st.sidebar.selectbox(
    "League",
    [f"All ({len(df_all):,} players)"] + available_leagues(df_all),
    index=0,
)
df_league = filter_by_league(df_all, league)

# ── Sidebar: Team filter (cascading) ────────────────────────────────────
team_list = available_teams(df_league, league)
teams_selected = st.sidebar.multiselect(
    "Team (multi-select)",
    ["All teams"] + team_list,
    default="All teams",
)
df_team = filter_by_team(df_league, teams_selected)

# ── Sidebar: Position filter (independent) ─────────────────────────────
pos_list = available_positions(df_team)
positions_selected = st.sidebar.multiselect(
    "Position",
    ["All positions"] + pos_list,
    default="All positions",
)
df_pos = filter_by_position(df_team, positions_selected)

# ── Sidebar: Role filter (independent) ─────────────────────────────────
role_list = available_roles(df_pos)
roles_selected = st.sidebar.multiselect(
    "Role",
    ["All roles"] + role_list,
    default="All roles",
)
df_final = filter_by_role(df_pos, roles_selected)

# ── Sidebar: Name search ──────────────────────────────────────────────────
name_query = st.sidebar.text_input("Search player (≥3 chars)")
df_search = filter_by_name(df_final, name_query)

# ── Main body ─────────────────────────────────────────────────────────────
st.success(f"Loaded {len(df_search):,} player rows")
st.dataframe(df_search.head(50), use_container_width=True)