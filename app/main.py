import streamlit as st
import os

st.set_page_config(page_title="Scout Hub 15/16", layout="wide")
st.title("Scout Hub 2015/16 – MVP")
st.info("🚧 Feature work in progress. Use the sidebar to navigate.")

db_url = os.environ.get("DB_URL", "sqlite:///data/players16.db")
