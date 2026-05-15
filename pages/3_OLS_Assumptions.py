import streamlit as st
import os
from pathlib import Path

st.set_page_config(page_title="OLS Assumptions Diagnostic", page_icon="🔬", layout="wide")

app_dir = Path(__file__).parent.parent / "apps" / "Linear regression" / "pages"
os.chdir(str(app_dir))

st.markdown("""
<style>
    [data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"],
    .st-emotion-cache-1dp5vir, .st-emotion-cache-1wrcr25 { display: none !important; }
    .stApp header, .stApp footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("[← Back to Linear Regression](/Linear_Regression)")

with open("1_Linear_Regression.py") as f:
    code = f.read()

exec(compile(code, "1_Linear_Regression.py", "exec"))
