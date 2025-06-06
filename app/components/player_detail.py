import streamlit as st
import pandas as pd

def render_detail(selected: pd.Series | None):
    with st.sidebar:
        st.markdown("---")
        if selected is None:
            st.info("Pick a player to see details ▶️")
            return
        st.image(
            "https://placehold.co/240x320?text=Photo",
            width=160,
            caption=selected["Name"],
        )
        st.subheader(selected["Name"])
        st.write(f"**Team:** {selected['Team']}")
        st.write(f"**Minutes:** {selected['Minutes']:,}")
