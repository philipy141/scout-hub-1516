# app/components/similar_panel.py
from __future__ import annotations
import streamlit as st
import pandas as pd
from app.services.similarity import get_similar
from app.services.logos import club_logo

def render_similar(current_row: pd.Series, df_all: pd.DataFrame) -> None:
    """
    Show a 5-row panel of the most similar players.
    When the user clicks a player name, we stash the new player_id into
    st.session_state["selected_player_id"] so main.py re-renders the drawer.
    """
    if current_row is None:
        return

    sim_df = get_similar(df_all, player_id=int(current_row.name), n=5)

    
    # ---- nice formatting ------------------------------------------------
    sim_df["Δ-score"] = (1.0 - sim_df["similarity"]).round(3)  # lower is better
    sim_df.rename(columns={"player": "Player", "team": "Team"}, inplace=True)

    # ---- UI -------------------------------------------------------------
    st.subheader("Similar players")

    for _, r in sim_df.iterrows():
        col_logo, col_name, col_delta = st.columns([1, 5, 2])
        with col_logo:
            st.image(club_logo(r["Team"]), width=32)
        with col_name:
            if st.button(r["Player"], key=f"sim_{int(r['player_id'])}"):
                st.session_state["selected_player_id"] = int(r["player_id"])
        with col_delta:
            st.write(f"Δ {r['Δ-score']:.3f}")
