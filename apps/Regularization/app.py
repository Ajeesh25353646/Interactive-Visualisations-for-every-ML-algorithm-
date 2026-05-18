import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import Ridge, Lasso, ElasticNet, LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline

st.title("⚖️ The Regularization Showdown: All Models Compared")

st.markdown("""
To truly understand Regularization, we need to compare **OLS (No Penalty)** against **Ridge**, **Lasso**, and **Elastic Net** at the same time.
Watch how the **Weight Values** in the table below change as you increase the penalty ($\alpha$).
""")

# --- Sidebar: Global Controls ---
with st.sidebar:
    st.header("🛠️ Global Parameters")
    alpha = st.slider("Penalty Intensity (Alpha)", 0.001, 2.0, 0.1, format="%.3f")
    complexity = st.slider("Model Complexity (Degree)", 1, 12, 7)
    noise = st.slider("Data Noise", 0.1, 2.0, 0.6)
    
    st.divider()
    st.subheader("Elastic Net Specific")
    l1_ratio = st.slider("L1 Ratio (0=Ridge, 1=Lasso)", 0.0, 1.0, 0.5)

# --- Data Generation ---
np.random.seed(42)
X = np.sort(5 * np.random.rand(40, 1), axis=0)
y = np.sin(X).ravel() + np.random.normal(0, noise, X.shape[0])
X_plot = np.linspace(0, 5, 100).reshape(-1, 1)

# --- Model Definitions ---
poly = PolynomialFeatures(complexity, include_bias=False)
scaler = StandardScaler()

models = {
    "Plain OLS": LinearRegression(),
    "Ridge (L2)": Ridge(alpha=alpha),
    "Lasso (L1)": Lasso(alpha=alpha, max_iter=10000),
    "Elastic Net": ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=10000)
}

# --- Training and Data Collection ---
results = {}
weights_data = {}

for name, model_obj in models.items():
    pipe = make_pipeline(poly, scaler, model_obj)
    pipe.fit(X, y)
    results[name] = pipe.predict(X_plot)
    # Store weights (rounded for readability)
    weights_data[name] = pipe.steps[-1][1].coef_

# Create a Weights DataFrame
weight_df = pd.DataFrame(weights_data)
weight_df.index = [f"X^{i+1}" for i in range(complexity)]

# --- Visualisation ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📈 Prediction Comparison")
    fig = go.Figure()
    
    # Actual Data
    fig.add_trace(go.Scatter(x=X.ravel(), y=y, mode='markers', name='Actual Data', marker=dict(color='black', opacity=0.4)))
    
    # Model Lines
    colors = {"Plain OLS": "red", "Ridge (L2)": "blue", "Lasso (L1)": "green", "Elastic Net": "orange"}
    for name, y_pred in results.items():
        fig.add_trace(go.Scatter(x=X_plot.ravel(), y=y_pred, mode='lines', name=name, line=dict(color=colors[name], width=2)))
    
    fig.update_layout(height=500, template="plotly_white", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📋 Weight (Coefficient) Table")
    st.write("Compare how each model treats the same features.")
    
    # Stylized DataFrame
    def color_zeros(val):
        color = 'red' if abs(val) < 1e-4 else 'black'
        return f'color: {color}'

    st.dataframe(weight_df.style.applymap(color_zeros).format("{:.4f}"), height=450)

st.divider()

# --- Summary Metrics ---
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

def get_metrics(name):
    w = weight_df[name]
    zeros = np.sum(np.abs(w) < 1e-4)
    avg_mag = np.mean(np.abs(w))
    return zeros, avg_mag

for i, name in enumerate(models.keys()):
    zeros, mag = get_metrics(name)
    with [m_col1, m_col2, m_col3, m_col4][i]:
        st.metric(name, f"Zeroed: {zeros}", delta=f"Avg weight: {mag:.3f}", delta_color="inverse")

# --- Mathematical Deep Dive ---
st.divider()
st.header("🔬 Mathematical Deep Dive (Interview Ready)")

m_tab1, m_tab2, m_tab3 = st.tabs(["📐 The Objective Function", "💎 Why Lasso hits Zero?", "🎓 Interview Checklist"])

with m_tab1:
    st.markdown("All regularization models modify the **Ordinary Least Squares (OLS)** cost function:")
    st.latex(r"Cost = \text{MSE} + \text{Penalty}")
    
    st.markdown("#### 1. Ridge ($L_2$ Regularization)")
    st.latex(r"J(\theta) = \text{MSE} + \alpha \sum_{i=1}^{n} \theta_i^2")
    st.write("The penalty is the **sum of squares** of the weights. This is also known as Tikhonov regularization.")

    st.markdown("#### 2. Lasso ($L_1$ Regularization)")
    st.latex(r"J(\theta) = \text{MSE} + \alpha \sum_{i=1}^{n} |\theta_i|")
    st.write("The penalty is the **sum of absolute values** of the weights.")

    st.markdown("#### 3. Elastic Net (Hybrid)")
    st.latex(r"J(\theta) = \text{MSE} + r\alpha \sum | \theta | + \frac{1-r}{2}\alpha \sum \theta^2")
    st.write("A convex combination of $L_1$ and $L_2$. The parameter $r$ (l1_ratio) controls the mix.")

with m_tab2:
    st.write("### Geometric Intuition: The Diamond vs. The Circle")
    st.markdown("""
    Interviewers often ask: **'Why does Lasso zero out weights but Ridge doesn't?'**
    
    Imagine the constraint region for your weights:
    *   **Ridge ($L_2$):** The constraint is a **Circle** ($w_1^2 + w_2^2 \leq t$). The OLS error contours usually touch this circle at a point where both weights are small but non-zero.
    *   **Lasso ($L_1$):** The constraint is a **Diamond** ($|w_1| + |w_2| \leq t$). Because of the sharp 'corners' on the axes, the error contours are very likely to hit a corner first.
    *   **Result:** When the contour hits a corner, one of the coordinates is **exactly zero**. This is why Lasso performs automatic feature selection.
    """)

with m_tab3:
    st.info("""
    **Checklist for your next interview:**
    *   **Term to use:** 'Sparsity'. Lasso induces sparsity in the model.
    *   **Term to use:** 'Shrinkage'. Both models perform shrinkage, but Ridge is more stable.
    *   **Key Parameter:** $\alpha$ (Alpha). In some textbooks, this is called $\lambda$ (Lambda). It controls the tradeoff between fitting the data and keeping weights small.
    *   **Scaling:** Always mention that **Feature Scaling (Standardization)** is mandatory before regularization. If features have different scales, the penalty will unfairly target features with smaller numerical ranges.
    *   **Multicollinearity:** If features are highly correlated, Ridge is preferred because it shares the 'credit' between them. Lasso might just pick one and discard the others.
    """)
