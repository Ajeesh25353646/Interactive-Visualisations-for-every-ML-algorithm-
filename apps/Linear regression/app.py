import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Linear Regression Visualizer", layout="wide")

st.title("📈 Mastering Linear Regression: From Intuition to Interview")

# --- Introduction ---
st.markdown("""
### 1. The Story: Predicting the Future
Imagine you are a real estate agent. You notice that as the **Size of a House** (Square Feet) increases, the **Price** usually goes up. 
Linear Regression is simply the math of finding the **'Best Fitting Line'** through these data points so we can predict the price of a house we've never seen before.
""")

# --- Sidebar: User Controls ---
with st.sidebar:
    st.header("🛠️ Controls")
    st.markdown("Adjust these to see how the 'Best Fit' line changes.")

    noise = st.slider("Data Randomness (Noise)", 0, 50, 20)
    n_points = st.slider("Number of Houses", 10, 100, 50)

    st.divider()
    st.subheader("Manual Line Fitting")
    st.info("Try to move these sliders to get the lowest Error (MSE)!")
    user_m = st.slider("Your Slope (Slope)", 0.0, 5.0, 1.0, step=0.1)
    user_c = st.slider("Your Intercept (Starting Price)", 0, 100, 10)
    
    show_optimal = st.toggle("Show Optimal Line (The Truth)", value=False)

    st.divider()
    st.markdown("---")
    st.subheader("🔬 Advanced Topics")
    st.markdown("Want to master OLS assumptions?")
    if st.button("📊 OLS Assumptions Diagnostic", use_container_width=True, key="adv_sidebar", help="Check homoscedasticity, normality, VIF, and autocorrelation"):
        st.switch_page("pages/2_🔬_OLS_Assumptions.py")

# --- Data Generation ---
np.random.seed(42)
X = np.linspace(10, 100, n_points)
# Real relationship: y = 2x + 15 + noise
y = 2 * X + 15 + np.random.normal(0, noise, n_points)

# Calculate User Predictions
y_user = user_m * X + user_c
residuals = y - y_user
mse = np.mean(residuals**2)

# Calculate Optimal Line (The "Truth")
model = LinearRegression()
model.fit(X.reshape(-1, 1), y)
optimal_m = model.coef_[0]
optimal_c = model.intercept_
y_optimal = model.predict(X.reshape(-1, 1))
optimal_mse = np.mean((y - y_optimal)**2)

# --- Visualisation ---
col1, col2 = st.columns([2, 1])

with col1:
    fig = go.Figure()

    # Data Points
    fig.add_trace(go.Scatter(x=X, y=y, mode='markers', name='Actual Houses', marker=dict(color='blue', size=8)))

    # User Line
    fig.add_trace(go.Scatter(x=X, y=y_user, mode='lines', name='Your Prediction Line', line=dict(color='red', width=3)))

    # Optimal Line
    if show_optimal:
        fig.add_trace(go.Scatter(x=X, y=y_optimal, mode='lines', name='Optimal Line (OLS)', line=dict(color='green', width=2, dash='dash')))

    # Residuals (The vertical lines)
    for i in range(len(X)):
        fig.add_trace(go.Scatter(
            x=[X[i], X[i]], y=[y[i], y_user[i]],
            mode='lines',
            line=dict(color='rgba(255,0,0,0.2)', width=1),
            showlegend=False,
            hoverinfo='none'
        ))

    fig.update_layout(
        title=f"Your Equation: Price = {user_m:.1f} * Size + {user_c}",
        xaxis_title="Size (Sq Ft)",
        yaxis_title="Price ($1000s)",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 The Scoreboard")
    st.metric("Your Error (MSE)", f"{mse:.2f}")
    st.metric("Best Possible Error", f"{optimal_mse:.2f}")
    
    if mse <= optimal_mse * 1.05:
        st.success("🎯 Amazing! You found the Best Fit line!")
    elif mse < 1000:
        st.warning("🤏 Close! Adjust the sliders a bit more.")
    else:
        st.error("📉 High Error. Try to align the red line with the dots.")

st.divider()

# --- Conceptual Deep Dive ---
st.header("🧠 Conceptual Deep Dive")

tab1, tab2, tab3 = st.tabs(["📏 Residuals", "📉 The Cost Function", "🤖 Model Training"])

with tab1:
    st.markdown("""
    ### What are Residuals?
    Look at the faint red vertical lines in the graph above. Those are **Residuals**.
    *   **Actual Value ($y$):** The blue dot (What the house actually sold for).
    *   **Predicted Value ($\hat{y}$):** The red line (What your model guessed).
    *   **Residual ($e$):** The distance between them ($y - \hat{y}$).
    """)
    
    # Residual Distribution
    res_fig = go.Figure(data=[go.Histogram(x=residuals, nbinsx=15, marker_color='red', opacity=0.7)])
    res_fig.update_layout(
        title="Distribution of Residuals (Errors)",
        xaxis_title="Residual Value",
        yaxis_title="Count",
        template="plotly_white",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(res_fig, use_container_width=True)
    
    st.markdown("""
    **Interview Tip:** "In a perfect model, the sum of residuals is zero and they are normally distributed (Bell Curve)."
    """)

with tab2:
    st.markdown("""
    ### Mean Squared Error (MSE)
    How do we know if a line is "good"? We use a **Loss Function**.
    The most common is **MSE**. We take every residual, **square it** (to remove negative signs and penalize big errors more), and find the average.
    
    $$MSE = \\frac{1}{n} \\sum_{i=1}^{n} (y_i - \hat{y}_i)^2$$
    """)

with tab3:
    st.markdown("""
    ### How does the computer learn? (Gradient Descent)
    You manually adjusted the sliders. A computer uses **Gradient Descent**.
    1.  It starts with random $m$ and $c$.
    2.  It calculates the MSE.
    3.  It calculates the "Slope" of the error (calculus!) to see which direction makes the error smaller.
    4.  It takes a small step (Learning Rate) in that direction.
    5.  Repeat until the error is as small as possible.
    """)

# --- Interview Prep ---
st.header("🎯 Interview Quick-Fire Prep")

st.info("""
**Q: What are the assumptions of Linear Regression?**
1. **Linearity:** The relationship is a straight line.
2. **Independence:** Data points aren't related to each other (e.g. time series).
3. **Homoscedasticity:** The error (residual) is consistent across the line.
4. **Normality:** Residuals follow a normal distribution.
5. **No Multicollinearity:** Independent variables are not highly correlated.

**Q: What is the difference between Error and Residual?**
*   **Error:** Theoretical difference between observed and *true* population value.
*   **Residual:** Practical difference between observed and *estimated* (predicted) value.
""")

st.divider()

# --- Link to Advanced Diagnostics ---
st.markdown("""
### 🔬 Want to Go Deeper?

Check out the **OLS Assumptions Diagnostic** page (in sidebar ↑) for interactive visualizations on:
- 📊 **Residual Plots** - Check homoscedasticity (funnel shape detection)
- 📈 **Q-Q Plots** - Verify normality of residuals
- 🔢 **VIF Calculator** - Detect multicollinearity
- ⏱️ **Durbin-Watson** - Test for autocorrelation
""")

col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
with col_back2:
    if st.button("🔬 Open Advanced Diagnostics", use_container_width=True, key="adv_footer"):
        st.switch_page("pages/2_🔬_OLS_Assumptions.py")
