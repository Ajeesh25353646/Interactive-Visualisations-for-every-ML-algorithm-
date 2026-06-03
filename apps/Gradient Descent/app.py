import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os

st.title("📉 Gradient Descent: The Path to Optimization")

st.markdown("""
Gradient Descent is an optimization algorithm used to minimize a loss function by iteratively moving in the direction of steepest descent. 
Adjust the parameters in the sidebar to see how they impact the learning path!
""")

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Hyperparameters")
    
    gd_type = st.selectbox("GD Variant", ["Batch Gradient Descent", "Stochastic GD (SGD)", "Mini-Batch GD"])
    
    lr = st.select_slider("Learning Rate (η)", 
                          options=[0.0001, 0.001, 0.01, 0.1, 0.5, 1.0, 2.0], 
                          value=0.1)
    
    iterations = st.slider("Max Iterations", 10, 500, 100)
    
    st.divider()
    st.subheader("Starting Point")
    start_x = st.slider("Initial X value", -5.0, 5.0, -4.0)
    
    st.divider()
    if gd_type == "Mini-Batch GD":
        batch_size = st.slider("Batch Size", 2, 32, 8)
    else:
        batch_size = 1

# --- Function Definitions ---
# f(x) = x^2 (The Loss Function)
def loss_function(x):
    return x**2

# f'(x) = 2x (The Gradient)
def gradient_function(x):
    return 2*x

# --- Data Generation for Smooth Curves ---
x_vals = np.linspace(-5, 5, 400)
y_vals = loss_function(x_vals)

# --- Simulation Logic ---
history_x = [start_x]
history_y = [loss_function(start_x)]

curr_x = start_x

# Seed for reproducibility in SGD/Mini-batch noise
np.random.seed(42)

for i in range(iterations):
    # Base Gradient
    grad = gradient_function(curr_x)
    
    # Add noise based on GD type
    if gd_type == "Stochastic GD (SGD)":
        # Simulate single point noise (High Variance)
        noise = np.random.normal(0, 2.0)
        grad += noise
    elif gd_type == "Mini-Batch GD":
        # Simulate mini-batch noise (Moderate Variance)
        noise = np.random.normal(0, 0.8)
        grad += noise
    
    # Update Rule
    curr_x = curr_x - lr * grad
    
    # Boundary constraints to prevent plotting issues
    if abs(curr_x) > 100: 
        st.error("Divergence Detected! Your learning rate is likely too high.")
        break
        
    history_x.append(curr_x)
    history_y.append(loss_function(curr_x))
    
    # Convergence Check
    if abs(grad) < 0.001 and gd_type == "Batch Gradient Descent":
        break

# --- Visualisation ---
col1, col2 = st.columns([2, 1])

with col1:
    fig = go.Figure()
    
    # 1. The Loss Function Curve
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Loss Function J(θ)', line=dict(color='gray', dash='dot')))
    
    # 2. The Path Taken
    fig.add_trace(go.Scatter(x=history_x, y=history_y, mode='lines+markers', 
                             name='Learning Path', 
                             marker=dict(size=6, color='red'),
                             line=dict(width=2, color='red')))
    
    # 3. Final Point
    fig.add_trace(go.Scatter(x=[history_x[-1]], y=[history_y[-1]], mode='markers', 
                             name='Final Position', 
                             marker=dict(size=12, color='blue', symbol='star')))

    fig.update_layout(
        title=f"Path of {gd_type}",
        xaxis_title="Parameter (θ)",
        yaxis_title="Loss J(θ)",
        template="plotly_white",
        height=500
    )
    st.plotly_chart(fig, width="stretch")

with col2:
    st.subheader("📊 Convergence Stats")
    st.write(f"**Iterations:** {len(history_x) - 1}")
    st.write(f"**Final Loss:** {history_y[-1]:.6f}")
    st.write(f"**Final θ:** {history_x[-1]:.4f}")
    
    if history_y[-1] < 0.01:
        st.success("Target Reached! Model has converged.")
    elif abs(history_x[-1]) > 5:
        st.warning("Model Diverged. Try a lower learning rate.")
    else:
        st.info("Still searching... try more iterations.")

    st.divider()
    st.markdown("""
    ### Intuition:
    - **Batch GD:** Smooth, direct path. 
    - **SGD:** High variance. The path "jitters" because each step is based on a noisy estimate.
    - **Learning Rate:**
        - Small: Slow but steady.
        - Large: Might bounce back and forth or fly off the graph!
    """)

# --- Interactive 3D Explorer ---
st.divider()
st.header("🎮 Interactive 3D Loss Landscape")
st.write("Explore how different optimizers (Adam, Momentum, etc.) navigate complex landscapes like Saddle Points and local minima.")

# Load and embed the HTML file
_this_dir = os.environ.get("ST_APP_DIR") or os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(_this_dir, "Gradient Descent.html")
if os.path.exists(html_file_path):
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    st.iframe(html_content, height=800, scrolling=True)
else:
    st.error("HTML visualisation file not found.")

# --- Interview Deep Dive ---
st.divider()
st.header("🔬 Interview Deep Dive")

tab1, tab2, tab3 = st.tabs(["📐 Mathematical Foundation", "🚀 Optimizers & Momentum", "🎓 Common Questions"])

with tab1:
    st.markdown("### The Core Equation:")
    st.markdown("The weight update rule is:")
    st.latex(r"\theta_{new} = \theta_{old} - \eta \cdot \nabla J(\theta)")
    
    st.markdown("**Why the minus sign?**")
    st.markdown("The gradient $\\nabla J(\\theta)$ points in the direction of the steepest *ascent*. To find the minimum, we must move in the *opposite* direction.")
    
    st.markdown("**Feature Scaling Impact:**")
    st.markdown("Without normalization, if one feature has a much larger range than another, the loss surface becomes an elongated ellipse. Gradient descent will oscillate back and forth across the narrow dimension, taking a long time to reach the center.")

with tab2:
    st.markdown("### Overcoming Challenges:")
    st.markdown("1. **Momentum:**")
    st.markdown("Adds a fraction $\\gamma$ of the previous update to the current one.")
    st.latex(r"v_t = \gamma v_{t-1} + \eta \nabla J(\theta)")
    st.latex(r"\theta = \theta - v_t")
    st.markdown("*Intuition:* Helps \"roll over\" local minima and speeds up convergence in flat regions.")
    
    st.markdown("2. **Adam (Adaptive Moment Estimation):**")
    st.markdown("Computes adaptive learning rates for each parameter. It stores an exponentially decaying average of past gradients (like momentum) and past squared gradients (like RMSProp).")

with tab3:
    st.markdown("""
    ### High-Frequency Interview Questions:
    * **Q: Does Gradient Descent always find the Global Minimum?**
      * *A:* For **convex** functions (like Linear Regression loss), yes. For **non-convex** functions (like Neural Networks), it might get stuck in a local minimum or a saddle point.
    * **Q: What is a Saddle Point?**
      * *A:* A point where the gradient is zero, but it's a minimum in one dimension and a maximum in another. In high-dimensional spaces, saddle points are much more common than local minima.
    * **Q: Why is Mini-Batch GD preferred over Batch or SGD?**
      * *A:* It strikes a balance: it's more stable than SGD and more computationally efficient than Batch GD because it leverages vectorized operations on GPUs.
    """)
