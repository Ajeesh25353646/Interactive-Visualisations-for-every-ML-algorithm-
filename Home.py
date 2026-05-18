import streamlit as st

st.set_page_config(
    page_title="ML Algorithms Visualized",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Syne:wght@400;500;600;700;800&display=swap');

:root {
    --bg-primary: #13161B;
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
    --border-hover: #8B5CF6;
    --font-display: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
    color-scheme: dark;
}

.skip-link {
  position: absolute; top: -100%; left: 50%; transform: translateX(-50%);
  z-index: 9999; padding: 8px 16px; background: var(--accent-1); color: white;
  border-radius: 0 0 8px 8px; font-family: var(--font-body); font-size: 14px;
  text-decoration: none;
}
.skip-link:focus { top: 0; }

#MainMenu, header, footer, .stAppDeployButton,
.stActionButton, .viewerBadge_container__1QSob,
.stToolbar, .stDecoration, .stAppToolbar,
.st-emotion-cache-1dp5vir, .st-emotion-cache-1wrcr25,
.st-emotion-cache-zq5wmm, .st-emotion-cache-1aez1c7,
.st-emotion-cache-1qprp7y {
    display: none !important;
}
section[data-testid="stSidebar"], .stSidebar, .css-1d391kg, [data-testid="stSidebarContent"] { display: none !important; }
.st-emotion-cache-1wmy9hl, .st-emotion-cache-1oe6wy8 { display: none !important; }

.stApp, .main, .block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    min-width: 100% !important;
    width: 100% !important;
    background: var(--bg-primary) !important;
}
.main > div { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
.element-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
.stHorizontalBlock { gap: 0 !important; padding: 0 48px !important; margin: 0 !important; max-width: 100% !important; }
.stVerticalBlock { gap: 0 !important; }
.row-widget { padding: 0 !important; margin: 0 !important; }
body { background: var(--bg-primary) !important; color: var(--text-primary) !important; font-family: var(--font-body); }

.top-nav {
    display: flex; justify-content: space-between; align-items: center;
    padding: 20px 48px; border-bottom: 1px solid var(--border);
}
.nav-brand { font-family: var(--font-display); font-weight: 700; font-size: 20px; color: var(--text-primary); }
.nav-links { display: flex; gap: 24px; align-items: center; }
.nav-links a { color: var(--text-muted); text-decoration: none; font-size: 14px; transition: color 0.2s; }
.nav-links a:hover { color: var(--text-primary); }
.nav-links .nav-cta {
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    color: white !important; padding: 8px 16px; border-radius: 8px; font-weight: 600;
}

.hero {
    position: relative; min-height: 75vh; display: flex;
    align-items: center; justify-content: center; text-align: center;
    overflow: hidden; padding: 0 24px;
}
.hero-bg { position: absolute; inset: 0; z-index: 0; }
.hero-bg::before {
    content: ''; position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 30%, rgba(124,101,193,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 70%, rgba(99,102,241,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(124,101,193,0.04) 0%, transparent 50%);
    animation: breathe 8s ease-in-out infinite alternate;
}
.hero-bg::after {
    content: ''; position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
    background-size: 60px 60px;
}
@keyframes breathe {
    0% { opacity: 0.6; transform: scale(1); }
    100% { opacity: 1; transform: scale(1.05); }
}
.hero-content { position: relative; z-index: 1; max-width: 900px; }
.hero-title {
    font-family: var(--font-display); font-weight: 700;
    font-size: clamp(28px, 4.5vw, 56px); line-height: 1.15;
    margin: 0 0 4px 0; color: var(--text-primary);
}
.hero-title:last-of-type { margin-bottom: 16px; }
.gradient-text {
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-subtitle {
    font-size: clamp(15px, 1.6vw, 18px); color: var(--text-muted);
    line-height: 1.5; margin-bottom: 32px; max-width: 580px;
    margin-left: auto; margin-right: auto;
}
.hero-cta {
    display: inline-block;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    color: white !important; text-decoration: none !important;
    font-family: var(--font-display); font-weight: 600; font-size: 16px;
    padding: 16px 40px; border-radius: 12px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 0 30px rgba(124,101,193,0.2);
}
.hero-cta:hover { transform: translateY(-2px); box-shadow: 0 0 50px rgba(124,101,193,0.4); }

.section-wrapper { padding: 0 48px 40px; }
.section-title {
    font-family: var(--font-display); font-weight: 700;
    font-size: clamp(24px, 3vw, 36px); text-align: center;
    margin-bottom: 48px; padding-top: 60px; color: var(--text-primary);
}
.section-title::after {
    content: ''; display: block; width: 60px; height: 3px;
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    margin: 16px auto 0; border-radius: 2px;
}
.category-label {
    font-family: var(--font-display); font-weight: 600; font-size: 20px;
    color: var(--text-muted); margin-bottom: 24px; padding: 0 12px;
}

.viz-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 28px 24px;
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease, background 0.3s ease; height: 100%;
    display: flex; flex-direction: column;
    margin-bottom: 16px;
}
.viz-card:hover {
    background: var(--bg-card-hover); border-color: var(--border-hover);
    transform: translateY(-4px); box-shadow: 0 8px 40px rgba(124,101,193,0.15);
}
.card-icon { font-size: 32px; margin-bottom: 10px; line-height: 1; }
.card-title {
    font-family: var(--font-display); font-weight: 600;
    font-size: 17px; color: var(--text-primary); margin-bottom: 8px;
}
.card-badge {
    display: inline-block; font-size: 11px; font-weight: 600;
    padding: 3px 10px; border-radius: 20px; margin-bottom: 10px; width: fit-content;
}
.card-badge.live {
    background: rgba(34,211,161,0.1); color: var(--accent-green);
    border: 1px solid rgba(34,211,161,0.2);
}
.card-badge.coming-soon {
    background: rgba(107,114,128,0.1); color: var(--text-muted);
    border: 1px solid rgba(107,114,128,0.2);
}
.card-desc { font-size: 14px; color: var(--text-muted); line-height: 1.5; flex-grow: 1; margin-bottom: 12px; }

.card-link { text-decoration: none; color: inherit; display: block; border-radius: 16px; margin-bottom: 16px; transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease, background 0.3s ease; } .card-link:hover .viz-card { background: var(--bg-card-hover) !important; border-color: var(--border-hover) !important; transform: translateY(-4px) !important; box-shadow: 0 8px 40px rgba(124,101,193,0.15) !important; } .st-emotion-cache-1xarl3l, .st-emotion-cache-15hul8a { display: none !important; }

.coming-soon-placeholder {
    text-align: center; color: var(--text-dim); font-size: 13px;
    padding: 10px; border: 1px dashed var(--border); border-radius: 8px; margin-top: auto;
}

.features-grid {
    display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px; padding: 0 48px 60px; max-width: 1100px; margin: 0 auto;
}
.feature-card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: 16px; padding: 32px 24px; text-align: center;
    transition: border-color 0.3s;
}
.feature-card:hover { border-color: rgba(124,101,193,0.3); }
.feature-icon { font-size: 32px; margin-bottom: 14px; }
.feature-title {
    font-family: var(--font-display); font-weight: 600;
    font-size: 17px; color: var(--text-primary); margin-bottom: 8px;
}
.feature-desc { font-size: 14px; color: var(--text-muted); line-height: 1.5; }

.cta-section { text-align: center; padding: 80px 48px; border-top: 1px solid var(--border); }
.cta-title {
    font-family: var(--font-display); font-weight: 700;
    font-size: clamp(24px, 3vw, 36px); color: var(--text-primary); margin-bottom: 12px;
}
.cta-subtitle { font-size: 18px; color: var(--text-muted); margin-bottom: 32px; }
.cta-buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.cta-secondary {
    display: inline-block; background: transparent;
    color: var(--text-primary) !important; text-decoration: none !important;
    font-family: var(--font-display); font-weight: 600; font-size: 16px;
    padding: 16px 40px; border-radius: 12px;
    border: 1px solid var(--border); transition: border-color 0.2s, background 0.2s;
}
.cta-secondary:hover { border-color: var(--accent-1); background: rgba(124,101,193,0.05); }

.footer { text-align: center; padding: 32px 48px; border-top: 1px solid var(--border); font-size: 13px; color: var(--text-dim); }
.footer a { color: var(--text-muted); text-decoration: none; transition: color 0.2s; }
.footer a:hover { color: var(--accent-1); }
.footer-hiring { margin-top: 12px; font-size: 15px; color: var(--text-muted); }
.footer-hiring a { color: var(--accent-2) !important; font-weight: 600; }

/* ─── CARD ENTRY ANIMATION ─── */
@keyframes cardFadeIn {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}

.viz-card, .card-link {
    animation: cardFadeIn 0.4s ease forwards;
}

[data-testid="column"]:nth-child(1) .card-link,
[data-testid="column"]:nth-child(1) .viz-card { animation-delay: 0.05s; }
[data-testid="column"]:nth-child(2) .card-link,
[data-testid="column"]:nth-child(2) .viz-card { animation-delay: 0.10s; }
[data-testid="column"]:nth-child(3) .card-link,
[data-testid="column"]:nth-child(3) .viz-card { animation-delay: 0.15s; }

/* ─── DECORATIVE SECTION ART ─── */
.section-art { display: block; margin: 0 auto 16px; }

@media (max-width: 768px) {
    .top-nav { padding: 16px 24px; flex-direction: column; gap: 12px; }
    .section-wrapper { padding: 0 16px 24px; }
    .stHorizontalBlock { padding: 0 16px !important; }
    .features-grid { padding: 0 16px 40px; }
    .cta-section { padding: 48px 16px; }
    .footer { padding: 24px; }
}

@media (prefers-reduced-motion: reduce) {
  .hero-bg::before { animation: none !important; }
  .viz-card, .card-link { animation: none !important; }
  .hero-cta:hover { transform: none !important; }
  .viz-card:hover { transform: none !important; }
  .card-link:hover .viz-card { transform: none !important !important; }
}

:focus-visible {
  outline: 2px solid var(--accent-1);
  outline-offset: 2px;
}
.nav-links a:focus-visible, .hero-cta:focus-visible, .cta-secondary:focus-visible,
.footer a:focus-visible {
  outline: 2px solid var(--accent-1);
  outline-offset: 2px;
  border-radius: 4px;
}
</style>
""")

st.markdown("""
<a href="#main-content" class="skip-link">Skip to main content</a>
<nav class="top-nav" aria-label="Main navigation">
    <div class="nav-brand">🎯 ML Visualized</div>
    <div class="nav-links">
        <a href="https://github.com/Ajeesh25353646" target="_blank" rel="noopener noreferrer">GitHub</a>
        <a href="https://linkedin.com/in/ajeeshgarg" target="_blank" rel="noopener noreferrer">LinkedIn</a>
        <a href="mailto:gargajeesh@gmail.com" class="nav-cta">Hiring? Let's Talk</a>
    </div>
</nav>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-bg"></div>
    <div class="hero-content" id="main-content">
        <div class="hero-title">See <span class="gradient-text">ML</span>. Understand <span class="gradient-text">ML</span>.</div>
        <div class="hero-title">Ace the Interview.</div>
        <p class="hero-subtitle">
            Interactive visualizations for every core ML concept — from Regularization to Transformers.<br>
            Tweak parameters, see algorithms respond in real-time. No signup. Free.
        </p>
        <a href="#explore" class="hero-cta">Start Exploring →</a>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div id="explore" class="section-title">Explore Algorithms</div>', unsafe_allow_html=True)

# ─── CORE ML ───
st.markdown('<div class="section-wrapper">', unsafe_allow_html=True)
st.markdown("""
<svg class="section-art" viewBox="0 0 120 24" width="120" height="24" aria-hidden="true">
    <circle cx="15" cy="18" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="35" cy="14" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="55" cy="16" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="75" cy="8" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="95" cy="10" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="110" cy="6" r="2" fill="#8B5CF6" opacity="0.3"/>
    <line x1="8" y1="20" x2="115" y2="5" stroke="#8B5CF6" stroke-width="1" opacity="0.4"/>
</svg>
""", unsafe_allow_html=True)
st.markdown('<div class="category-label">Core ML</div>', unsafe_allow_html=True)

core_apps = [
    ("📈", "Linear Regression", "live", "Interactive slope/intercept fitting. Residuals, MSE, and full OLS assumptions diagnostic."),
    ("⚖️", "Regularization", "coming-soon", "Ridge, Lasso, ElasticNet — see penalty strength change coefficients in real-time."),
    ("📉", "Gradient Descent", "coming-soon", "Batch, SGD, Mini-Batch — watch the optimization path change with learning rate."),
    ("📊", "Evaluation Metrics", "coming-soon", "Confusion Matrix, ROC/PR Curves, Threshold Optimization with interactive puzzles."),
    ("🎯", "Bias-Variance Tradeoff", "coming-soon", "Polynomial degree explorer. Watch underfitting become overfitting in real-time."),
    ("🧶", "K-Means Clustering", "coming-soon", "Lloyd's Algorithm step-by-step. Voronoi diagrams. The Elbow Method."),
]

r1 = st.columns(3)
for i, (icon, name, status, desc) in enumerate(core_apps[:3]):
    with r1[i]:
        if status == "live":
            st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
        else:
            st.markdown(f"""
            <div class="viz-card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{name}</div>
                <div class="card-badge {status}">○ Coming Soon</div>
                <div class="card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

r2 = st.columns(3)
for i, (icon, name, status, desc) in enumerate(core_apps[3:]):
    with r2[i]:
        if status == "live":
            st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
        else:
            st.markdown(f"""
            <div class="viz-card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{name}</div>
                <div class="card-badge {status}">○ Coming Soon</div>
                <div class="card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

# ─── SUPERVISED ───
st.markdown("""
<svg class="section-art" viewBox="0 0 120 24" width="120" height="24" aria-hidden="true">
    <circle cx="15" cy="18" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="35" cy="14" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="55" cy="16" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="75" cy="8" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="95" cy="10" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="110" cy="6" r="2" fill="#8B5CF6" opacity="0.3"/>
    <line x1="8" y1="20" x2="115" y2="5" stroke="#8B5CF6" stroke-width="1" opacity="0.4"/>
</svg>
""", unsafe_allow_html=True)
st.markdown('<div class="category-label" style="margin-top: 32px;">Supervised Learning</div>', unsafe_allow_html=True)

supervised_apps = [
    ("🏷️", "Classification", "coming-soon", "KNN, SVM, Naive Bayes — decision boundary explorer with live comparison."),
    ("🌲", "Random Forest", "coming-soon", "Gini vs Entropy, tree explorer, ensemble demo with OOB error."),
    ("📈", "Gradient Boosting", "coming-soon", "Residual learning step-by-step. XGBoost vs LightGBM vs CatBoost."),
    ("🔮", "Clustering Algorithms", "coming-soon", "DBSCAN, Hierarchical, GMM — compare algorithms on the same dataset."),
]

r3 = st.columns(3)
for i, (icon, name, status, desc) in enumerate(supervised_apps[:3]):
    with r3[i]:
        if status == "live":
            st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
        else:
            st.markdown(f"""
            <div class="viz-card"><div class="card-icon">{icon}</div><div class="card-title">{name}</div><div class="card-badge {status}">○ Coming Soon</div><div class="card-desc">{desc}</div></div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

r4 = st.columns(3)
with r4[0]:
    icon, name, status, desc = supervised_apps[3]
    if status == "live":
        st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
    else:
        st.markdown(f"""
        <div class="viz-card"><div class="card-icon">{icon}</div><div class="card-title">{name}</div><div class="card-badge {status}">○ Coming Soon</div><div class="card-desc">{desc}</div></div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

# ─── ADVANCED ───
st.markdown("""
<svg class="section-art" viewBox="0 0 120 24" width="120" height="24" aria-hidden="true">
    <circle cx="15" cy="18" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="35" cy="14" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="55" cy="16" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="75" cy="8" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="95" cy="10" r="2" fill="#8B5CF6" opacity="0.3"/>
    <circle cx="110" cy="6" r="2" fill="#8B5CF6" opacity="0.3"/>
    <line x1="8" y1="20" x2="115" y2="5" stroke="#8B5CF6" stroke-width="1" opacity="0.4"/>
</svg>
""", unsafe_allow_html=True)
st.markdown('<div class="category-label" style="margin-top: 32px;">Deep Learning & Advanced</div>', unsafe_allow_html=True)

advanced_apps = [
    ("🧠", "Neural Networks", "coming-soon", "Backpropagation visualizer, activation functions, capacity & overfitting playground."),
    ("🔍", "CNN — Convolutional Nets", "coming-soon", "Receptive field calculator, parameter counter, VGG architecture explorer."),
    ("🤖", "Transformers & Attention", "coming-soon", "Transformer explainer with GPT-2 inference. See attention heads in action."),
    ("🔬", "PCA — Principal Components", "coming-soon", "Eigenvalues, explained variance, projection — see dimensions collapse in real-time."),
    ("📐", "Dim. Reduction", "coming-soon", "PCA vs UMAP vs Isomap. Compare manifold learning side-by-side."),
    ("🎨", "Stable Diffusion", "coming-soon", "Diffusion explainer with architecture deep dive and scheduler lab."),
    ("🚀", "Deployment Ready", "coming-soon", "Linear Regression with OLS diagnostics. Production-ready Streamlit structure."),
]

r5 = st.columns(3)
for i, (icon, name, status, desc) in enumerate(advanced_apps[:3]):
    with r5[i]:
        if status == "live":
            st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
        else:
            st.markdown(f"""<div class="viz-card"><div class="card-icon">{icon}</div><div class="card-title">{name}</div><div class="card-badge {status}">○ Coming Soon</div><div class="card-desc">{desc}</div></div>""", unsafe_allow_html=True)
            st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

r6 = st.columns(3)
for i, (icon, name, status, desc) in enumerate(advanced_apps[3:6]):
    with r6[i]:
        if status == "live":
            st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
        else:
            st.markdown(f"""<div class="viz-card"><div class="card-icon">{icon}</div><div class="card-title">{name}</div><div class="card-badge {status}">○ Coming Soon</div><div class="card-desc">{desc}</div></div>""", unsafe_allow_html=True)
            st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

r7 = st.columns(3)
with r7[0]:
    icon, name, status, desc = advanced_apps[6]
    if status == "live":
        st.page_link("pages/1_Linear_Regression.py", label=f"{icon} {name}\n\n● Live\n\n{desc}", use_container_width=True)
    else:
        st.markdown(f"""<div class="viz-card"><div class="card-icon">{icon}</div><div class="card-title">{name}</div><div class="card-badge {status}">○ Coming Soon</div><div class="card-desc">{desc}</div></div>""", unsafe_allow_html=True)
        st.markdown('<div class="coming-soon-placeholder">Coming Soon</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── FEATURES ───
st.markdown('<div class="section-title">What Makes This Different</div>', unsafe_allow_html=True)

st.markdown("""
<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon">🎮</div>
        <div class="feature-title">Scenario-Based Puzzles</div>
        <div class="feature-desc">Diagnose real ML problems from loss curves and plots — not just flashcards.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">📐</div>
        <div class="feature-title">Interactive Visualizations</div>
        <div class="feature-desc">Tweak sliders, change parameters, see algorithms respond in real-time.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">💬</div>
        <div class="feature-title">200+ Interview Q&A</div>
        <div class="feature-desc">Curated answers with mathematical foundations. Not memorization — understanding.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <div class="feature-title">Free, No Signup</div>
        <div class="feature-desc">Just open and learn. No account, no paywall, no data collection.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── CTA ───
st.markdown("""
<div class="cta-section">
    <h2 class="cta-title">Ready to see ML like never before?</h2>
    <p class="cta-subtitle">Start with Linear Regression — more visualizations added every week.</p>
    <div class="cta-buttons">
        <a href="#explore" class="hero-cta">Explore Algorithms →</a>
        <a href="https://github.com/Ajeesh25353646/Interactive-Visualisations-for-every-ML-algorithm-" target="_blank" rel="noopener noreferrer" class="cta-secondary">Star on GitHub</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── FOOTER ───
st.markdown("""
<div class="footer">
    <p>Built with Python, Streamlit, D3.js, and ☕</p>
    <p><a href="https://linkedin.com/in/ajeeshgarg" target="_blank" rel="noopener noreferrer">LinkedIn</a> · <a href="https://github.com/Ajeesh25353646" target="_blank" rel="noopener noreferrer">GitHub</a></p>
    <p class="footer-hiring"><strong>Hiring an ML Engineer?</strong> <a href="mailto:gargajeesh@gmail.com">Let's talk →</a></p>
</div>
""", unsafe_allow_html=True)
