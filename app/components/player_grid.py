import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


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

def render_grid(df: pd.DataFrame):
    gb = GridOptionsBuilder.from_dataframe(df)

    # Correct way to configure each column
    gb.configure_column("Name", header_name="Player Name", sortable=True)
    gb.configure_column("Team", header_name="Club", sortable=True)
    gb.configure_column("Minutes", type=["numericColumn"], sortable=True)

    # Optional: Set default behavior
    gb.configure_default_column(resizable=True, filter=True)

    grid_response = AgGrid(
        df,
        gridOptions=gb.build(),  # ✅ This should now be a proper dict
        height=480,
        theme="alpine",
    )

    selected_rows = grid_response["selected_rows"]
    if selected_rows:
        return pd.Series(selected_rows[0])
    return None