import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from services.data_loader import load_players_df
from services.filter_utils import (
    available_leagues, available_teams, available_positions, available_roles,
    apply_all_filters,
)
from components.player_detail import render_detail   # ← keeps your drawer

# ─────────────────────── Page config ─────────────────────────────────────
st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")

# ─────────────────────── Load dataset ────────────────────────────────────
df_all = load_players_df(force=True)

# ─────────────────────── Sidebar filters ────────────────────────────────
st.sidebar.header("Filters")

league = st.sidebar.selectbox(
    "League",
    options=["All"] + available_leagues(df_all),
    index=0,
)

team_options = available_teams(df_all, league)
teams = st.sidebar.multiselect(
    "Teams",
    options=["All teams"] + team_options,
    default="All teams",
)

pos_options = available_positions(df_all)
positions = st.sidebar.multiselect(
    "Positions",
    options=["All positions"] + pos_options,
    default="All positions",
)

role_options = available_roles(df_all)
roles = st.sidebar.multiselect(
    "Roles",
    options=["All roles"] + role_options,
    default="All roles",
)

search_name = st.sidebar.text_input("Search by name (≥3 chars)", value="")

# ─────────────────────── Apply filters ──────────────────────────────────
df_search = apply_all_filters(df_all, league, teams, positions, roles, search_name)
st.success(f"{len(df_search):,} players in view")

# ─────────────────────── Table (native) ─────────────────────────────────
# Pick the columns you want to display
cols_to_show = ["player", "team", "minutes_played"]  # add "age" if your table has it
st.dataframe(
    df_search[cols_to_show],
    use_container_width=True,
    hide_index=True,
)

# ─────────────────────── Player selector ────────────────────────────────
player_name = st.selectbox(
    "Select player to see details ▶️",
    ["—"] + df_search["player"].tolist(),
    index=0,
    key="player_selectbox",
)

if player_name != "—":
    player_row = df_search[df_search["player"] == player_name].iloc[0]
    render_detail(player_row)
