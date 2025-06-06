import streamlit as st
from app.services.data_loader import load_players_df

st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")

df = load_players_df()
st.success(f"Loaded {len(df):,} player rows")
st.info("🚧 Feature work in progress. Use the sidebar to navigate.")
