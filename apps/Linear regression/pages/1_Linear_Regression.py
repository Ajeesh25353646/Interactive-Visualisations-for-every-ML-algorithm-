import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats
from sklearn.linear_model import LinearRegression



st.title("🔬 Linear Regression: OLS Assumptions Diagnostic")

st.markdown("""
### The 5 Core OLS Assumptions

For Linear Regression to produce valid, reliable results, five key assumptions must be met:

| # | Assumption | What It Means | How to Check |
|---|------------|---------------|--------------|
| 1 | **Linearity** | Relationship between X and y is linear | Residual plot (no U-shape) |
| 2 | **Independence** | Observations are independent | Durbin-Watson statistic |
| 3 | **Homoscedasticity** | Constant variance of residuals | Residual plot (no funnel) |
| 4 | **Normality** | Residuals follow normal distribution | Q-Q plot |
| 5 | **No Multicollinearity** | Features aren't highly correlated | VIF (Variance Inflation Factor) |

---

**💡 Interview Tip:** "When asked about linear regression assumptions, always mention all 5 and explain how you'd diagnose violations."
""")

st.divider()

# Navigation
st.markdown("### Choose a Diagnostic Tool")

st.divider()

# Create tabs for each diagnostic
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Residual Plot (Homoscedasticity)",
    "📈 Q-Q Plot (Normality)",
    "🔢 VIF Calculator (Multicollinearity)",
    "⏱️ Durbin-Watson (Autocorrelation)"
])

# =============================================================================
# TAB 1: RESIDUAL PLOT - HOMOSCEDASTICITY
# =============================================================================
with tab1:
    st.header("📊 Residual Plot: Checking Homoscedasticity")
    
    st.markdown("""
    ### What is Homoscedasticity?
    
    **Homoscedasticity** means the variance of residuals is **constant** across all levels of the predicted values.
    
    - ✅ **Homoscedastic** (good): Residuals spread evenly → Random scatter
    - ❌ **Heteroscedastic** (bad): Residuals form a funnel shape → Variance changes
    
    **Why it matters:** Heteroscedasticity makes confidence intervals and hypothesis tests unreliable.
    """)
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("🛠️ Residual Plot Controls")
        
        violation_type = st.radio(
            "Violation Type",
            ["Random (Homoscedastic)", "Funnel (Heteroscedastic)", "U-Shape (Non-linear)"],
            key="residual_violation"
        )
        
        n_points = st.slider("Number of Points", 50, 500, 100, key="residual_n")
        noise_level = st.slider("Noise Level", 0.1, 3.0, 1.0, key="residual_noise")
        outlier_count = st.slider("Add Outliers", 0, 10, 0, key="residual_outliers")
    
    # Generate data based on violation type
    np.random.seed(42)
    X = np.linspace(0, 10, n_points)
    
    if violation_type == "Random (Homoscedastic)":
        # Constant variance
        y = 2 * X + 5 + np.random.normal(0, noise_level, n_points)
    elif violation_type == "Funnel (Heteroscedastic)":
        # Variance increases with X
        variance = 0.5 + 0.3 * X
        y = 2 * X + 5 + np.random.normal(0, variance * noise_level, n_points)
    else:  # U-Shape
        # Non-linear relationship
        y = 0.3 * X**2 - 3 * X + 10 + np.random.normal(0, noise_level * 0.5, n_points)
    
    # Add outliers
    if outlier_count > 0:
        outlier_indices = np.random.choice(n_points, outlier_count, replace=False)
        y[outlier_indices] += np.random.choice([-1, 1], outlier_count) * noise_level * 5
    
    # Fit model and calculate residuals
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), y)
    y_pred = model.predict(X.reshape(-1, 1))
    residuals = y - y_pred
    
    # Create the residual plot
    fig = go.Figure()
    
    # Residuals scatter
    fig.add_trace(go.Scatter(
        x=y_pred,
        y=residuals,
        mode='markers',
        name='Residuals',
        marker=dict(color='#3b82f6', size=6, opacity=0.6),
        hovertemplate='Predicted: %{x:.2f}<br>Residual: %{y:.2f}<extra></extra>'
    ))
    
    # Zero line
    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Line")
    
    # Add trend line to show pattern
    from sklearn.linear_model import LinearRegression as LR
    trend_model = LR()
    trend_model.fit(y_pred.reshape(-1, 1), residuals)
    trend_pred = trend_model.predict(y_pred.reshape(-1, 1))
    
    fig.add_trace(go.Scatter(
        x=y_pred,
        y=trend_pred,
        mode='lines',
        name='Trend',
        line=dict(color='green', width=3),
        showlegend=True
    ))
    
    fig.update_layout(
        title="Residuals vs Predicted Values",
        xaxis_title="Predicted Values (ŷ)",
        yaxis_title="Residuals (y - ŷ)",
        template="plotly_white",
        height=500,
        hovermode='closest'
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Diagnostics")
        
        # Breusch-Pagan test (simplified simulation)
        # In practice, use statsmodels: sm.stats.diagnostic.het_breuschpagan()
        residual_sq = residuals ** 2
        bp_corr = np.corrcoef(y_pred, residual_sq)[0, 1]
        bp_stat = abs(bp_corr) * 10
        
        st.metric("Breusch-Pagan Statistic (approx)", f"{bp_stat:.3f}")
        
        # Interpretation
        if violation_type == "Random (Homoscedastic)":
            st.success("✅ **Homoscedastic**: Residuals show random scatter. Assumption met!")
            st.info("Ideal: Points randomly scattered around zero with no pattern.")
        elif violation_type == "Funnel (Heteroscedastic)":
            st.error("❌ **Heteroscedastic**: Funnel shape detected. Variance increases with predictions.")
            st.warning("Fix: Try log transformation, weighted least squares, or robust regression.")
        else:
            st.error("❌ **Non-linearity**: U-shape indicates non-linear relationship.")
            st.warning("Fix: Add polynomial features or use non-linear model.")
        
        st.divider()
        
        st.markdown("### Interview Q&A")
        st.info("""
        **Q: How do you check homoscedasticity?**
        
        **A:** Plot residuals vs predicted values. Look for:
        - ✅ Random scatter = homoscedastic (good)
        - ❌ Funnel shape = heteroscedastic (bad)
        
        Formal test: **Breusch-Pagan test** (p < 0.05 indicates heteroscedasticity).
        
        **Q: What causes heteroscedasticity?**
        
        **A:** Common causes:
        - Outliers in the data
        - Missing important predictors
        - Non-linear relationships
        - Data from different populations
        """)

# =============================================================================
# TAB 2: Q-Q PLOT - NORMALITY
# =============================================================================
with tab2:
    st.header("📈 Q-Q Plot: Checking Normality of Residuals")
    
    st.markdown("""
    ### What is a Q-Q Plot?
    
    A **Quantile-Quantile (Q-Q) plot** compares the distribution of residuals to a theoretical normal distribution.
    
    - ✅ **Normal**: Points follow the 45° reference line
    - ❌ **Non-normal**: Points deviate from the line (S-shape, curves)
    
    **Why it matters:** Normality is needed for valid hypothesis tests and confidence intervals.
    """)
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("🛠️ Q-Q Plot Controls")
        
        skewness = st.slider("Skewness", -2.0, 2.0, 0.0, 0.1, key="qq_skew")
        kurtosis = st.slider("Kurtosis (Tail Weight)", -1.0, 3.0, 0.0, 0.1, key="qq_kurt")
        n_points = st.slider("Number of Points", 50, 500, 100, key="qq_n")
        show_reference = st.checkbox("Show Reference Line", value=True, key="qq_ref")
    
    # Generate residuals with controlled skewness and kurtosis
    np.random.seed(42)
    
    # Use skew-normal distribution
    from scipy.stats import skewnorm, t
    
    # Combine skewness and kurtosis effects
    if abs(skewness) < 0.1 and abs(kurtosis) < 0.1:
        # Normal distribution
        residuals_qq = np.random.normal(0, 1, n_points)
    else:
        # Skewed distribution
        residuals_qq = skewnorm.rvs(a=skewness*3, size=n_points)
        # Add heavy tails if kurtosis is high
        if kurtosis > 0.5:
            heavy_tails = t.rvs(df=3, size=n_points) * (kurtosis / 2)
            residuals_qq = (residuals_qq + heavy_tails) / 2
    
    residuals_qq = residuals_qq * (1 + kurtosis * 0.3)
    
    # Calculate theoretical quantiles
    sorted_residuals = np.sort(residuals_qq)
    n = len(sorted_residuals)
    theoretical_quantiles = stats.norm.ppf((np.arange(n) + 0.5) / n)
    
    # Create Q-Q plot
    fig = go.Figure()
    
    # Data points
    fig.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sorted_residuals,
        mode='markers',
        name='Sample Quantiles',
        marker=dict(color='#3b82f6', size=6, opacity=0.6),
        hovertemplate='Theoretical: %{x:.2f}<br>Sample: %{y:.2f}<extra></extra>'
    ))
    
    # Reference line
    if show_reference:
        # Fit line through quartiles
        q1_idx, q3_idx = n // 4, 3 * n // 4
        slope = (sorted_residuals[q3_idx] - sorted_residuals[q1_idx]) / (theoretical_quantiles[q3_idx] - theoretical_quantiles[q1_idx])
        intercept = sorted_residuals[q1_idx] - slope * theoretical_quantiles[q1_idx]
        ref_line_y = slope * theoretical_quantiles + intercept
        
        fig.add_trace(go.Scatter(
            x=theoretical_quantiles,
            y=ref_line_y,
            mode='lines',
            name='Reference Line',
            line=dict(color='red', dash='dash', width=2)
        ))
    
    fig.update_layout(
        title="Q-Q Plot: Residuals vs Normal Distribution",
        xaxis_title="Theoretical Quantiles (Normal)",
        yaxis_title="Sample Quantiles (Residuals)",
        template="plotly_white",
        height=500,
        hovermode='closest'
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Normality Tests")
        
        # Shapiro-Wilk test
        shapiro_stat, shapiro_p = stats.shapiro(residuals_qq[:5000])  # Limit for speed
        st.metric("Shapiro-Wilk p-value", f"{shapiro_p:.4f}")
        
        # Anderson-Darling test
        ad_result = stats.anderson(residuals_qq, dist='norm')
        ad_stat = ad_result.statistic
        
        st.metric("Anderson-Darling Statistic", f"{ad_stat:.4f}")
        
        # Verdict
        st.divider()
        st.subheader("Verdict")
        
        if shapiro_p > 0.05:
            st.success(f"✅ **Residuals appear normally distributed** (p = {shapiro_p:.3f} > 0.05)")
            st.info("Points should closely follow the reference line.")
        else:
            st.error(f"❌ **Residuals are NOT normally distributed** (p = {shapiro_p:.3f} < 0.05)")
            if skewness > 0.5:
                st.warning("Issue: Right-skewed (positive skew). Try log or square root transformation.")
            elif skewness < -0.5:
                st.warning("Issue: Left-skewed (negative skew). Consider feature transformation.")
            if kurtosis > 1:
                st.warning("Issue: Heavy tails (high kurtosis). Check for outliers.")
            elif kurtosis < -0.5:
                st.warning("Issue: Light tails (low kurtosis). Distribution is too flat.")
        
        st.divider()
        
        st.markdown("### Interview Q&A")
        st.info("""
        **Q: How do you check if residuals are normal?**
        
        **A:** Use a **Q-Q plot**. If residuals are normal, points follow the 45° reference line.
        
        Formal tests:
        - **Shapiro-Wilk test** (p > 0.05 = normal)
        - **Anderson-Darling test**
        - **Kolmogorov-Smirnov test**
        
        **Q: What if residuals are not normal?**
        
        **A:** Try:
        - Transform the target variable (log, sqrt, Box-Cox)
        - Remove outliers
        - Use a different model (robust regression, GLM)
        - Collect more data (CLT helps with large n)
        """)

# =============================================================================
# TAB 3: VIF CALCULATOR - MULTICOLLINEARITY
# =============================================================================
with tab3:
    st.header("🔢 VIF Calculator: Detecting Multicollinearity")
    
    st.markdown("""
    ### What is VIF?
    
    **Variance Inflation Factor (VIF)** measures how much the variance of a coefficient is inflated due to multicollinearity.
    
    $$\\text{VIF}_i = \\frac{1}{1 - R_i^2}$$
    
    Where $R_i^2$ is the R² from regressing feature $i$ on all other features.
    
    | VIF Value | Interpretation |
    |-----------|----------------|
    | VIF = 1   | No multicollinearity |
    | 1 < VIF < 5 | Moderate multicollinearity |
    | VIF ≥ 5 | High multicollinearity (concerning) |
    | VIF ≥ 10 | Severe multicollinearity (must fix) |
    
    **Why it matters:** Multicollinearity makes coefficients unstable and hard to interpret.
    """)
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("🛠️ VIF Controls")
        
        n_features = st.slider("Number of Features", 3, 6, 4, key="vif_n")
        correlation_strength = st.slider("Correlation Strength", 0.0, 0.99, 0.3, 0.05, key="vif_corr")
        add_highly_correlated = st.checkbox("Add Highly Correlated Pair", value=False, key="vif_high_corr")
        n_samples = st.slider("Sample Size", 50, 500, 100, key="vif_samples")
    
    # Generate correlated features
    np.random.seed(42)
    
    # Create correlation matrix
    if n_features == 3:
        corr_matrix = np.array([
            [1.0, correlation_strength, correlation_strength * 0.5],
            [correlation_strength, 1.0, correlation_strength * 0.5],
            [correlation_strength * 0.5, correlation_strength * 0.5, 1.0]
        ])
    elif n_features == 4:
        corr_matrix = np.array([
            [1.0, correlation_strength, correlation_strength * 0.5, correlation_strength * 0.3],
            [correlation_strength, 1.0, correlation_strength * 0.5, correlation_strength * 0.3],
            [correlation_strength * 0.5, correlation_strength * 0.5, 1.0, correlation_strength * 0.3],
            [correlation_strength * 0.3, correlation_strength * 0.3, correlation_strength * 0.3, 1.0]
        ])
    elif n_features == 5:
        corr_matrix = np.array([
            [1.0, correlation_strength, correlation_strength * 0.5, correlation_strength * 0.3, 0.2],
            [correlation_strength, 1.0, correlation_strength * 0.5, correlation_strength * 0.3, 0.2],
            [correlation_strength * 0.5, correlation_strength * 0.5, 1.0, correlation_strength * 0.3, 0.2],
            [correlation_strength * 0.3, correlation_strength * 0.3, correlation_strength * 0.3, 1.0, 0.2],
            [0.2, 0.2, 0.2, 0.2, 1.0]
        ])
    else:  # 6 features
        corr_matrix = np.array([
            [1.0, correlation_strength, correlation_strength * 0.5, correlation_strength * 0.3, 0.2, 0.1],
            [correlation_strength, 1.0, correlation_strength * 0.5, correlation_strength * 0.3, 0.2, 0.1],
            [correlation_strength * 0.5, correlation_strength * 0.5, 1.0, correlation_strength * 0.3, 0.2, 0.1],
            [correlation_strength * 0.3, correlation_strength * 0.3, correlation_strength * 0.3, 1.0, 0.2, 0.1],
            [0.2, 0.2, 0.2, 0.2, 1.0, 0.1],
            [0.1, 0.1, 0.1, 0.1, 0.1, 1.0]
        ])
    
    # Add highly correlated pair
    if add_highly_correlated and n_features >= 2:
        corr_matrix[0, 1] = 0.95
        corr_matrix[1, 0] = 0.95
    
    # Ensure positive semi-definite
    eigenvalues = np.linalg.eigvalsh(corr_matrix)
    if np.min(eigenvalues) < 0:
        corr_matrix += np.eye(n_features) * (abs(np.min(eigenvalues)) + 0.01)
    
    # Generate multivariate normal data
    from numpy.linalg import cholesky
    L = cholesky(corr_matrix)
    X = np.random.randn(n_samples, n_features) @ L.T
    
    # Create feature names
    feature_names = [f"Feature {i+1}" for i in range(n_features)]
    
    # Calculate VIF for each feature
    vif_values = []
    
    for i in range(n_features):
        # Regress feature i on all other features
        X_other = np.delete(X, i, axis=1)
        y_feature = X[:, i]
        
        reg = LinearRegression()
        reg.fit(X_other, y_feature)
        r_squared = reg.score(X_other, y_feature)
        
        vif = 1 / (1 - r_squared) if r_squared < 0.999 else float('inf')
        vif_values.append(vif)
    
    vif_df = pd.DataFrame({
        'Feature': feature_names,
        'VIF': vif_values
    })
    
    # Create visualizations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Correlation Heatmap")
        
        # Correlation heatmap
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=feature_names,
            y=feature_names,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix, 2),
            texttemplate='%{text}',
            textfont={"size": 12},
            hovertemplate='%{x} vs %{y}: %{z:.3f}<extra></extra>'
        ))
        
        fig_corr.update_layout(
            title="Feature Correlation Matrix",
            height=400,
            xaxis_title="Features",
            yaxis_title="Features"
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        st.subheader("📊 VIF Values")
        
        # VIF bar chart
        colors = ['green' if v < 5 else 'orange' if v < 10 else 'red' for v in vif_values]
        
        fig_vif = go.Figure(data=go.Bar(
            x=feature_names,
            y=vif_values,
            marker_color=colors,
            hovertemplate='%{x}: VIF = %{y:.2f}<extra></extra>'
        ))
        
        # Add threshold lines
        fig_vif.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="VIF = 5 (Concerning)")
        fig_vif.add_hline(y=10, line_dash="dash", line_color="red", annotation_text="VIF = 10 (Severe)")
        
        fig_vif.update_layout(
            title="Variance Inflation Factor (VIF)",
            xaxis_title="Features",
            yaxis_title="VIF Value",
            height=400,
            yaxis_range=[0, max(max(vif_values) * 1.2, 15)]
        )
        
        st.plotly_chart(fig_vif, use_container_width=True)
    
    st.divider()
    
    # Summary table
    st.subheader("📋 VIF Summary")
    
    vif_df_styled = vif_df.copy()
    vif_df_styled['Status'] = vif_df_styled['VIF'].apply(
        lambda x: '✅ OK' if x < 5 else '⚠️ Moderate' if x < 10 else '❌ Severe'
    )
    
    vif_df_styled['VIF'] = vif_df_styled['VIF'].round(3)
    
    st.dataframe(vif_df_styled, use_container_width=True, height=200)
    
    # --- NEW: Coefficient Stability Demo ---
    st.divider()
    st.subheader("🧪 Interactive: Coefficient Stability Demo")
    st.markdown("""
    **The "Stress Test":** Watch what happens to the coefficients when we add just a **tiny bit of random noise** (±1%) to the data. 
    If VIF is high, the coefficients will jump wildly!
    """)
    
    if st.button("🏃 Run Stress Test", use_container_width=True):
        # 1. Fit Original Model
        y_sim = X @ np.ones(n_features) + np.random.normal(0, 0.5, n_samples)
        reg1 = LinearRegression().fit(X, y_sim)
        coef1 = reg1.coef_
        
        # 2. Add 1% Noise and Re-fit
        X_noisy = X + np.random.normal(0, X.std(axis=0) * 0.01, X.shape)
        reg2 = LinearRegression().fit(X_noisy, y_sim)
        coef2 = reg2.coef_
        
        # Display Results
        stab_df = pd.DataFrame({
            'Feature': feature_names,
            'Original Coef': coef1,
            'Noisy Coef': coef2,
            'Change (%)': ((coef2 - coef1) / np.abs(coef1)) * 100
        }).set_index('Feature')
        
        stab_df['Original Coef'] = stab_df['Original Coef'].round(3)
        stab_df['Noisy Coef'] = stab_df['Noisy Coef'].round(3)
        stab_df['Change (%)'] = stab_df['Change (%)'].round(1).map('{:+.1f}%'.format)
        
        col_s1, col_s2 = st.columns([1.2, 0.8])
        with col_s1:
            st.write("**Coefficient Comparison**")
            st.dataframe(
                stab_df,
                column_config={
                    "Original Coef": st.column_config.NumberColumn(width="medium"),
                    "Noisy Coef": st.column_config.NumberColumn(width="medium"),
                    "Change (%)": st.column_config.TextColumn(width="medium"),
                },
                use_container_width=False
            )
        
        with col_s2:
            max_change = stab_df['Change (%)'].abs().max()
            if max_change > 50:
                st.error(f"😱 **Extreme Instability!** The coefficients changed by up to {max_change:.1f}%.")
                st.info("This is why Multicollinearity is dangerous: your model's 'importance' values are just luck!")
            elif max_change > 10:
                st.warning(f"⚠️ **Moderate Instability.** Max change: {max_change:.1f}%.")
            else:
                st.success(f"✅ **Stable Coefficients.** Max change: {max_change:.1f}%.")

    # Interpretation
    max_vif = max(vif_values)
    st.divider()
    st.subheader("📊 Interpretation")
    
    if max_vif < 5:
        st.success(f"✅ **No concerning multicollinearity** (Max VIF = {max_vif:.2f})")
        st.info("All VIF values are below 5. Coefficients should be stable and interpretable.")
    elif max_vif < 10:
        st.warning(f"⚠️ **Moderate multicollinearity detected** (Max VIF = {max_vif:.2f})")
        st.info("Consider removing or combining correlated features, or use regularization.")
    else:
        st.error(f"❌ **Severe multicollinearity** (Max VIF = {max_vif:.2f})")
        st.warning("""
        **Recommended fixes:**
        1. Remove one of the highly correlated features
        2. Combine correlated features (PCA, feature engineering)
        3. Use Ridge Regression (L2 regularization)
        4. Collect more data
        """)
    
    st.divider()
    
    st.markdown("### Interview Q&A")
    st.info("""
    **Q: What is VIF? How do you detect multicollinearity?**
    
    **A:** **VIF (Variance Inflation Factor)** measures how much a coefficient's variance is inflated due to correlation with other features.
    
    $$\\text{VIF} = \\frac{1}{1 - R^2}$$
    
    Where R² comes from regressing that feature on all others.
    
    **Thresholds:**
    - VIF < 5: Acceptable
    - VIF 5-10: Concerning
    - VIF > 10: Severe (must fix)
    
    **Q: What problems does multicollinearity cause?**
    
    **A:** 
    - Unstable coefficients (small data changes → large coefficient swings)
    - Hard to interpret feature importance
    - Inflated standard errors
    - Coefficients may have wrong signs
    
    **Q: How do you fix multicollinearity?**
    
    **A:**
    1. Remove one of the correlated features
    2. Combine features (PCA, create ratios/indices)
    3. Use **Ridge Regression** (shrinks correlated coefficients together)
    4. Collect more data
    5. Use domain knowledge to select one representative feature
    """)

# =============================================================================
# TAB 4: DURBIN-WATSON - AUTOCORRELATION
# =============================================================================
with tab4:
    st.header("⏱️ Durbin-Watson Statistic: Checking Autocorrelation")
    
    st.markdown("""
    ### What is Autocorrelation?
    
    **Autocorrelation** (or serial correlation) occurs when residuals are correlated with each other over time/order.
    
    This violates the **Independence** assumption of OLS.
    
    ### Durbin-Watson Statistic
    
    $$d = \\frac{\\sum_{i=2}^{n}(e_i - e_{i-1})^2}{\\sum_{i=1}^{n}e_i^2}$$
    
    | DW Value | Interpretation |
    |----------|----------------|
    | d ≈ 2    | No autocorrelation |
    | d < 1.5  | Positive autocorrelation (concerning) |
    | d > 2.5  | Negative autocorrelation (concerning) |
    | d = 0    | Perfect positive autocorrelation |
    | d = 4    | Perfect negative autocorrelation |
    
    **Why it matters:** Autocorrelation is common in time series and makes standard errors unreliable.
    """)
    
    # Sidebar controls
    with st.sidebar:
        st.subheader("🛠️ Durbin-Watson Controls")
        
        autocorr_strength = st.slider("Autocorrelation Strength", -1.0, 1.0, 0.0, 0.05, key="dw_strength")
        n_points = st.slider("Number of Points", 20, 200, 50, key="dw_n")
        noise_level = st.slider("Noise Level", 0.1, 2.0, 1.0, key="dw_noise")
        
        autocorr_type = st.radio(
            "Autocorrelation Type",
            ["None", "Positive", "Negative", "Seasonal"],
            key="dw_type"
        )
    
    # Generate residuals with controlled autocorrelation
    np.random.seed(42)
    
    if autocorr_type == "None":
        autocorr_strength = 0.0
        residuals_dw = np.random.normal(0, noise_level, n_points)
    elif autocorr_type == "Positive":
        # AR(1) process with positive autocorrelation
        residuals_dw = np.zeros(n_points)
        residuals_dw[0] = np.random.normal(0, noise_level)
        for i in range(1, n_points):
            residuals_dw[i] = abs(autocorr_strength) * residuals_dw[i-1] + np.random.normal(0, noise_level * (1 - abs(autocorr_strength)))
    elif autocorr_type == "Negative":
        # AR(1) process with negative autocorrelation
        residuals_dw = np.zeros(n_points)
        residuals_dw[0] = np.random.normal(0, noise_level)
        for i in range(1, n_points):
            residuals_dw[i] = -abs(autocorr_strength) * residuals_dw[i-1] + np.random.normal(0, noise_level * (1 - abs(autocorr_strength)))
    else:  # Seasonal
        # Seasonal pattern
        t = np.arange(n_points)
        seasonal = np.sin(2 * np.pi * t / 10) * noise_level
        residuals_dw = seasonal + np.random.normal(0, noise_level * 0.3, n_points)
    
    # Calculate Durbin-Watson statistic
    dw_numerator = np.sum(np.diff(residuals_dw) ** 2)
    dw_denominator = np.sum(residuals_dw ** 2)
    dw_statistic = dw_numerator / dw_denominator if dw_denominator > 0 else 2.0
    
    # Create visualization
    fig = go.Figure()
    
    # Residuals over time
    fig.add_trace(go.Scatter(
        x=list(range(n_points)),
        y=residuals_dw,
        mode='lines+markers',
        name='Residuals',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=4),
        hovertemplate='Order: %{x}<br>Residual: %{y:.3f}<extra></extra>'
    ))
    
    # Zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    # Highlight consecutive changes
    if n_points <= 50:  # Only show arrows for small datasets
        for i in range(1, min(n_points, 50)):
            fig.add_annotation(
                x=i,
                y=(residuals_dw[i-1] + residuals_dw[i]) / 2,
                ax=i-0.5,
                ay=residuals_dw[i-1],
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                showarrow=True,
                arrowhead=1,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor='rgba(239, 68, 68, 0.5)'
            )
    
    fig.update_layout(
        title="Residuals Over Time (Order)",
        xaxis_title="Observation Order",
        yaxis_title="Residual Value",
        template="plotly_white",
        height=400,
        hovermode='closest'
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Durbin-Watson Statistic")
        
        st.metric("Durbin-Watson d", f"{dw_statistic:.4f}")
        
        st.divider()
        
        # Interpretation gauge
        if dw_statistic < 1.5:
            st.error(f"❌ **Positive Autocorrelation** (d = {dw_statistic:.3f} < 1.5)")
            st.warning("Consecutive residuals tend to have the same sign.")
        elif dw_statistic > 2.5:
            st.error(f"❌ **Negative Autocorrelation** (d = {dw_statistic:.3f} > 2.5)")
            st.warning("Consecutive residuals tend to alternate signs.")
        elif dw_statistic < 1.8:
            st.warning(f"⚠️ **Possible Positive Autocorrelation** (d = {dw_statistic:.3f})")
        elif dw_statistic > 2.2:
            st.warning(f"⚠️ **Possible Negative Autocorrelation** (d = {dw_statistic:.3f})")
        else:
            st.success(f"✅ **No Autocorrelation** (d = {dw_statistic:.3f} ≈ 2)")
            st.info("Residuals appear independent.")
        
        st.divider()
        
        st.markdown("### Interpretation Guide")
        st.markdown("""
        | d Value | Autocorrelation |
        |---------|-----------------|
        | 0 - 1.5 | Positive (concerning) |
        | 1.5 - 1.8 | Possible positive |
        | 1.8 - 2.2 | None (good) |
        | 2.2 - 2.5 | Possible negative |
        | 2.5 - 4 | Negative (concerning) |
        """)
    
    st.divider()
    
    st.markdown("### Interview Q&A")
    st.info("""
    **Q: What is the Durbin-Watson statistic?**
    
    **A:** It tests for **autocorrelation** in residuals (whether consecutive residuals are correlated).
    
    $$d = \\frac{\\sum_{i=2}^{n}(e_i - e_{i-1})^2}{\\sum_{i=1}^{n}e_i^2}$$
    
    **Interpretation:**
    - d ≈ 2: No autocorrelation
    - d < 1.5: Positive autocorrelation (bad)
    - d > 2.5: Negative autocorrelation (bad)
    
    **Q: When is autocorrelation a problem?**
    
    **A:** Most common in **time series data** where observations are ordered by time.
    
    **Problems it causes:**
    - Standard errors are underestimated
    - t-statistics are inflated
    - Confidence intervals are too narrow
    - Hypothesis tests are unreliable
    
    **Q: How do you fix autocorrelation?**
    
    **A:**
    1. Add lagged variables (y_{t-1} as a feature)
    2. Use time series models (ARIMA, SARIMA)
    3. Add missing time-dependent features
    4. Use robust standard errors (Newey-West)
    5. Difference the data (use changes instead of levels)
    """)

# =============================================================================
# SUMMARY SECTION
# =============================================================================
st.divider()

st.header("📋 OLS Assumptions Checklist")

st.markdown("""
### Quick Reference for Interviews

When asked "How do you validate a linear regression model?", mention checking all 5 assumptions:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### ✅ Linearity
    - **Check:** Residual plot (no U-shape)
    - **Fix:** Add polynomial features, use non-linear model
    
    #### ✅ Independence  
    - **Check:** Durbin-Watson (d ≈ 2)
    - **Fix:** Add lagged variables, use time series models
    """)

with col2:
    st.markdown("""
    #### ✅ Homoscedasticity
    - **Check:** Residual plot (random scatter)
    - **Fix:** Log transform, weighted least squares, robust regression
    
    #### ✅ Normality
    - **Check:** Q-Q plot, Shapiro-Wilk test
    - **Fix:** Transform target, remove outliers
    """)

with col3:
    st.markdown("""
    #### ✅ No Multicollinearity
    - **Check:** VIF < 5 (acceptable), VIF < 10 (must)
    - **Fix:** Remove features, PCA, Ridge regression
    """)

st.divider()

st.info("""
### 🎯 Final Interview Tip

**Perfect answer structure:**

"When validating my linear regression model, I check all 5 OLS assumptions:

1. **Linearity** - I plot residuals vs predictions and look for patterns
2. **Independence** - I calculate Durbin-Watson statistic (should be ≈ 2)
3. **Homoscedasticity** - I check for funnel shapes in residual plots
4. **Normality** - I use Q-Q plots and Shapiro-Wilk test
5. **No Multicollinearity** - I calculate VIF for each feature (should be < 5)

If any assumption is violated, I apply appropriate fixes like transformations, regularization, or alternative models."
""")
