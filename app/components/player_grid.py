import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import hashlib

VISIBLE_COLS = ["player", "team", "minutes_played"]
NICE_NAMES   = {"player": "Name", "team": "Team", "minutes_played": "Minutes"}

@st.cache_data(show_spinner=False)
def _format_df(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[VISIBLE_COLS].copy()
    sub.rename(columns=NICE_NAMES, inplace=True)
    return sub

def render_grid(df: pd.DataFrame) -> pd.Series | None:
    ready = _format_df(df)

    # Generate a unique key based on the current dataframe index and shape
    df_key = hashlib.md5(pd.util.hash_pandas_object(ready).values).hexdigest()

    gb = GridOptionsBuilder.from_dataframe(ready)
    gb.configure_default_column(resizable=True, filter=True, sortable=True)

    grid_response = AgGrid(
        ready,
        gridOptions=gb.build(),
        height=480,
        theme="alpine",
        key=f"player_grid_{df_key}",  # 💡 unique key based on DF contents
    )

    rows = grid_response["selected_rows"]
    if rows:
        return pd.Series(rows[0])
    return None
