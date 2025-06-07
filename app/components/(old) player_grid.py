import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

VISIBLE_COLS = ["player", "team", "minutes_played"]
NICE_NAMES = {"player": "Name", "team": "Team", "minutes_played": "Minutes"}

# @st.cache_data(show_spinner=False)
def _format_df(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[VISIBLE_COLS].copy()
    sub.rename(columns=NICE_NAMES, inplace=True)
    return sub

def render_grid(df: pd.DataFrame, key: str = "player_grid_main") -> pd.Series | None:
    ready = _format_df(df)

    gb = GridOptionsBuilder.from_dataframe(ready)
    gb.configure_default_column(resizable=True, filter=True, sortable=True)
    gb.configure_selection("single")  # Enable row selection

    grid_response = AgGrid(
        ready,
        gridOptions=gb.build(),
        height=480,
        theme="alpine",
        key=key,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,

    )

    rows = grid_response["selected_rows"]

    if isinstance(rows, list) and len(rows) > 0:
        return pd.Series(rows[0])

    return None


