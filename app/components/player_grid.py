import streamlit as st
import pandas as pd

VISIBLE_COLS = ["player", "team", "minutes_played"]
NICE_NAMES   = {
    "player": "Name",
    "team": "Team",
    "minutes_played": "Minutes",
}

@st.cache_data(show_spinner=False)
def _format_df(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[VISIBLE_COLS].copy()
    sub.rename(columns=NICE_NAMES, inplace=True)
    return sub

def render_grid(df: pd.DataFrame):
    ready = _format_df(df)
    st.dataframe(
        ready,
        use_container_width=True,
        column_config={
            "Minutes": st.column_config.NumberColumn(format="%d"),
        },
        hide_index=True,
    )
