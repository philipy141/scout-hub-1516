import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from app.services.data_loader import load_players_df
from app.services.filter_utils import (
    available_leagues, available_teams, available_positions, available_roles,
    filter_by_league, filter_by_team, filter_by_position, filter_by_role,
    filter_by_name, apply_all_filters,
)
from app.components.player_grid import render_grid
from app.components.player_detail import render_detail   # optional drawer

st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")

# ─── Load full dataset ────────────────────────────────────────────────────
df_all = load_players_df(force=True)

# ─── Sidebar filters ──────────────────────────────────────────────────────
st.sidebar.header("Filters")

# League
league = st.sidebar.selectbox(
    "League",
    options=["All"] + available_leagues(df_all),
    index=0,
)

# Teams (cascading)
team_options = available_teams(df_all, league)
teams = st.sidebar.multiselect(
    "Teams",
    options=["All teams"] + team_options,
    default="All teams",
)

# Positions
pos_options = available_positions(df_all)
positions = st.sidebar.multiselect(
    "Positions",
    options=["All positions"] + pos_options,
    default="All positions",
)

# Roles
role_options = available_roles(df_all)
roles = st.sidebar.multiselect(
    "Roles",
    options=["All roles"] + role_options,
    default="All roles",
)

# Name search
search_name = st.sidebar.text_input("Search by name (≥3 chars)", value="")

# ─── Apply all filters in one shot ────────────────────────────────────────
df_search = apply_all_filters(df_all, league, teams, positions, roles, search_name)

st.success(f"{len(df_search):,} players in view")

# ─── Render interactive grid (single instance) ───────────────────────────
selected_player = render_grid(df_search, key="player_grid_main")
# one interactive grid ---------------------------------------------------
selected_now = render_grid(df_search, key="player_grid_main")

# keep selection across reruns (Cloud is slower → empty list on rerun)
if selected_now is not None:                       # ← NEW
    st.session_state["selected_player"] = selected_now  # ← NEW

player = st.session_state.get("selected_player")   # may be None first run
if player is not None:
    render_detail(player)
else:
    st.sidebar.info("Select a player row to see details ▶️")


# DEBUG LINE: print to console/log
st.write("Selected:", selected_player)

# ─── Optional player drawer / debug print ────────────────────────────────
if selected_player is not None:
    render_detail(selected_player)           # proper drawer
    # st.write("You selected:", selected_player["Name"])  # quick debug
else:
    st.sidebar.info("Select a player row to see details ▶️")

