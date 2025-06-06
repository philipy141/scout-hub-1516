import streamlit as st
from services.data_loader import load_players_df
from services.filter_utils import available_leagues, filter_by_league

st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")

df = load_players_df()
st.success(f"Loaded {len(df):,} player rows")
st.info("🚧 Feature work in progress. Use the sidebar to navigate.")

# ---- sidebar league selector ----
st.sidebar.header("Filters")
league_list = available_leagues(df)
all_label   = f"All ({len(df):,} players)"
selected_league = st.sidebar.selectbox(
    "League", [all_label] + league_list, index=0
)

df = filter_by_league(df, selected_league)

# ---- main body ----
st.success(f"Loaded {len(df):,} player rows")
st.dataframe(df.head(50))
