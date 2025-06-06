# app/components/player_detail.py
import streamlit as st
import pandas as pd

def render_detail(selected: pd.Series) -> None:
    """
    Show a simple player drawer / card.

    Parameters
    ----------
    selected : pd.Series
        The row returned from main.py, from the filtered df_search.
    """
    # --- left column: placeholder photo ----------------------------------
    with st.sidebar:
        st.image(
            "https://placehold.co/200x250?text=Photo",
            caption=selected["player"],
            use_column_width=True,
        )

    # --- right column: meta & quick stats --------------------------------
    st.subheader(selected["player"])
    st.markdown(f"**Team:** {selected['team']}")
    st.markdown(f"**Minutes played:** {selected['minutes_played']:.0f}")
    # add whatever else you like, e.g. goals/assists/position
