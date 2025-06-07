# app/main.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 1) Must be first Streamlit call
import streamlit as st
st.set_page_config(page_title="Scout Hub 15/16", layout="wide")

import pandas as pd
from services.data_loader import load_players_df
from services.filter_utils import (
    available_leagues,
    available_teams,
    available_positions,
    available_roles,
    apply_all_filters,
)
from services.percentiles import role_percentiles, load_radar_config
from services.radar_config import ROLE_MAP
from components.player_detail import render_detail
from app.components.role_benchmark import render_benchmark

# ─────────────── Load & Prepare Data ───────────────
df_all = load_players_df(force=True)
df_all["radar_role"] = df_all["role"].replace(ROLE_MAP)

# ─────────────── Sidebar Filters ───────────────
st.title("Scout Hub 2015/16 – MVP")
league = st.sidebar.selectbox("League", ["All"] + available_leagues(df_all))
teams = st.sidebar.multiselect("Teams", ["All teams"] + available_teams(df_all, league), default="All teams")
positions = st.sidebar.multiselect("Positions", ["All positions"] + available_positions(df_all), default="All positions")
roles = st.sidebar.multiselect("Roles", ["All roles"] + available_roles(df_all), default="All roles")
search_name = st.sidebar.text_input("Search by name (≥3 chars)")

df_search = apply_all_filters(df_all, league, teams, positions, roles, search_name)
st.success(f"{len(df_search):,} players in view")

# ─────────────── Table View ───────────────
cols_to_show = ["player", "team", "minutes_played"]
st.dataframe(df_search[cols_to_show], use_container_width=True, hide_index=True)

# ─────────────── Player Selector ───────────────
dropdown_options = ["—"] + df_search["player"].tolist()
player_name = st.selectbox(
    "Select player to see details ▶️",
    dropdown_options,
    key="player_selectbox",
)

player_row: pd.Series | None = None

if player_name != "—":
    player_row = df_search[df_search["player"] == player_name].iloc[0]


# ─────────────── Render Detail Drawer ───────────────
if player_row is not None:
    radar_cfg = load_radar_config()
    population = df_all[df_all["radar_role"] == player_row["radar_role"]]
    player_row["percentiles"] = role_percentiles(
        player_row, population, radar_cfg, role_key="radar_role"
    )
    render_detail(player_row, df_all)

# after computing player_row["percentiles"]:
if player_row is not None:
    pop = df_all[df_all["radar_role"] == player_row["radar_role"]]
    metrics = load_radar_config()[ player_row["radar_role"] ]
    render_benchmark(player_row, pop, metrics, role_key="radar_role")