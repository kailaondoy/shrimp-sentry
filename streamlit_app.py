import streamlit as st

home = st.Page("home.py", title="🦐 Shrimp Sentry")
front = st.Page("front.py", title="Screen Distance")
side = st.Page("side.py", title="Spine Angle")

pg = st.navigation([home, front, side])
pg.run()