import streamlit as st
import os
from pathlib import Path

st.set_page_config(layout="wide")

app_dir = Path(__file__).parent.parent / "visualisations" / "Regularization"
os.chdir(str(app_dir))

st.markdown("""
<style>
    [data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"],
    .st-emotion-cache-1dp5vir, .st-emotion-cache-1wrcr25 { display: none !important; }
    .stApp header, .stApp footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.caption("← [Back to Home](/)")

with open("app.py") as f:
    code = f.read()

exec(compile(code, "app.py", "exec"))
