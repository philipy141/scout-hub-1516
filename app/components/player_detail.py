import streamlit as st
import pandas as pd
from app.services.radar import build_radar, save_png
from app.services.similarity import get_similar, SIM_COLUMNS
import io


# NOTE ──────────────────────────────────────────────────────────────
# df_all is now OPTIONAL so legacy tests that call render_detail(None)
# without a second arg will no longer raise TypeError.
# ───────────────────────────────────────────────────────────────────
def render_detail(
    selected: pd.Series | None,
    df_all: pd.DataFrame | None = None,
) -> None:
    """Draw the side-drawer card for a selected player."""
    if selected is None:
        st.sidebar.info("Select a player row to see details ▶️")
        return

    # ── sidebar photo & meta ───────────────────────────────────────
    with st.sidebar:
        st.image(
            "https://placehold.co/180x220?text=Photo",
            caption=selected["player"],
            use_column_width=True,
        )
        st.markdown(f"**{selected['player']} – {selected['team']}**")
        st.markdown(f"**Position – {selected['position']}**")
        st.markdown(f"**Role – {selected['role']}**")
        st.markdown(f"**Goals – {selected['goals']}**")
        st.markdown(f"**Goals per 90 – {selected['goals_per90']}**")
        st.markdown(f"Minutes played: **{int(selected['minutes_played']):,}**")

    # ── radar ──────────────────────────────────────────────────────
    pct = selected.get("percentiles", {})

    if "percentiles" in selected and isinstance(selected["percentiles"], dict):
        # build the radar
        fig = build_radar(selected["percentiles"], title=f"{selected['player']} vs role")
        st.plotly_chart(fig, use_container_width=True)

        # export to PNG in‐memory
        img_bytes = fig.to_image(format="png", scale=2)  # bytes

        # sanitize player name & season
        player_slug = selected["player"].replace(" ", "_")
        season = "2015-16"  # or pull from your config/df if dynamic

        st.download_button(
            label="📥 Download radar as PNG",
            data=img_bytes,
            file_name=f"{player_slug}_{season}_radar.png",
            mime="image/png",
            help="Save this player’s radar chart to your computer",
        )


    # ── similar-players block (only if a full DF is provided) ─────
    if df_all is not None and all(col in df_all for col in SIM_COLUMNS):
            # --- Similar-players panel ---
            from app.components.similar_panel import render_similar
            render_similar(selected, df_all)
            
    # ── extra info (optional) ──────────────────────────────────────
    st.subheader(f"{selected['player']} – {selected['team']}")
    st.write("Minutes played:", int(selected["minutes_played"]))
