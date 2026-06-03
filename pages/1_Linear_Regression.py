import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Linear Regression | Interactive ML Visualization", page_icon="📈", layout="wide")

st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Syne:wght@400;500;600;700;800&display=swap">
<style>
:root {
    --bg-primary: #0F1117;
    --bg-card: #1A1E26;
    --bg-card-hover: #212631;
    --accent-1: #8B5CF6;
    --accent-2: #A78BFA;
    --accent-green: #34D399;
    --accent-warm: #F59E0B;
    --text-primary: #F1F5F9;
    --text-muted: #9CAAC5;
    --text-dim: #7885A0;
    --border: #2E3440;
    --font-display: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
    color-scheme: dark;
}
body, .stApp { background: var(--bg-primary) !important; color: var(--text-primary) !important; font-family: var(--font-body) !important; }
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown strong, .stMarkdown em { color: var(--text-primary) !important; font-family: var(--font-body) !important; }
h1, h2, h3, h4 { font-family: var(--font-display) !important; color: var(--text-primary) !important; }
.stSidebar { background: var(--bg-card) !important; }
.stSidebar .stSlider label, .stSidebar .stMarkdown, .stSidebar p, .stSidebar .stText { color: var(--text-primary) !important; }
.stSidebar .stDivider hr { border-color: var(--border) !important; }
.stSidebar .stAlert { background: rgba(139,92,246,0.1) !important; border-color: var(--accent-1) !important; color: var(--text-primary) !important; }
.stSidebar .stButton button { background: var(--accent-1) !important; color: white !important; border: none !important; font-family: var(--font-display) !important; }
.stSidebar .stButton button:hover { background: var(--accent-2) !important; }
.stSidebar .stCheckbox label { color: var(--text-primary) !important; }
.stSidebar .stToggle label { color: var(--text-primary) !important; }
.stSidebar .stMetric { background: var(--bg-card) !important; border-radius: 8px; padding: 12px; }
.stSidebar .stMetric label { color: var(--text-muted) !important; }
.stSidebar .stMetric div[data-testid="stMetricValue"] { color: var(--text-primary) !important; }
.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] { background: var(--bg-card) !important; border-radius: 8px 8px 0 0; }
.stTabs [aria-selected="true"] { background: var(--bg-card-hover) !important; }
.stTabs [data-baseweb="tab"] p { color: var(--text-primary) !important; }
.stTabs [data-baseweb="tab-panel"] { background: var(--bg-card) !important; border-radius: 0 0 8px 8px; }
.stTabs [data-baseweb="tab-panel"] .stMarkdown, .stTabs [data-baseweb="tab-panel"] p { color: var(--text-primary) !important; }
.stTabs [data-baseweb="tab-panel"] .stAlert { background: rgba(139,92,246,0.1) !important; border-color: var(--accent-1) !important; color: var(--text-primary) !important; }
.js-plotly-plot .plotly, .js-plotly-plot .plotly .main-svg { background: transparent !important; }
.js-plotly-plot .plotly .xtick text, .js-plotly-plot .plotly .ytick text { fill: var(--text-muted) !important; }
.js-plotly-plot .plotly .gtitle text { fill: var(--text-primary) !important; }
.js-plotly-plot .plotly .xtitle text, .js-plotly-plot .plotly .ytitle text { fill: var(--text-muted) !important; }
.js-plotly-plot .plotly .legend text { fill: var(--text-primary) !important; }
.block-container { padding-top: 2rem !important; }
.back-link { color: var(--accent-2) !important; text-decoration: none !important; font-size: 14px !important; font-family: var(--font-body) !important; }
.back-link:hover { color: var(--text-primary) !important; }
.stDivider hr { border-color: var(--border) !important; }
.stAlert { background: rgba(139,92,246,0.1) !important; border-color: var(--accent-1) !important; color: var(--text-primary) !important; }
.stAlert p { color: var(--text-primary) !important; }
.stSuccess { background: rgba(52,211,153,0.1) !important; border-color: var(--accent-green) !important; }
.stSuccess p { color: var(--accent-green) !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-color: var(--accent-warm) !important; }
.stWarning p { color: var(--accent-warm) !important; }
.stError { background: rgba(239,68,68,0.1) !important; border-color: #EF4444 !important; }
.stError p { color: #EF4444 !important; }
.stMetric label { color: var(--text-muted) !important; }
.stMetric div[data-testid="stMetricValue"] { color: var(--text-primary) !important; }
.stButton button { background: var(--accent-1) !important; color: white !important; border: none !important; font-family: var(--font-display) !important; border-radius: 8px !important; }
.stButton button:hover { background: var(--accent-2) !important; }

@media (max-width: 768px) {
  .block-container { padding-top: 1rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
  .stSidebar .stSlider label, .stSidebar .stMarkdown, .stSidebar p { font-size: 13px !important; }
  .stTabs [data-baseweb="tab"] { font-size: 13px !important; }
}
</style>
""")

app_dir = Path(__file__).parent.parent / "apps" / "Linear regression"

import sys
sys.path.insert(0, str(app_dir))

with open(app_dir / "app.py") as f:
    code = f.read()

exec(compile(code, "app.py", "exec"))
