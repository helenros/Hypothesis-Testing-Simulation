import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

st.title('Walk the Curve: Z-Test Hypothesis Testing Simulation')

# Persist current role and data in session state
if 'role' not in st.session_state:
    st.session_state.role = None
if 'sample_data' not in st.session_state:
    st.session_state.sample_data = None
if 'sample_mean' not in st.session_state:
    st.session_state.sample_mean = None
if 'se' not in st.session_state:
    st.session_state.se = None
if 'z_score' not in st.session_state:
    st.session_state.z_score = None
if 'alpha' not in st.session_state:
    st.session_state.alpha = 0.05
if 'critical_value' not in st.session_state:
    st.session_state.critical_value = stats.norm.ppf(1 - st.session_state.alpha/2)

# Sidebar Parameters
mu_0 = st.sidebar.number_input('Population Mean (μ₀)', value=2.0, step=0.1)
sigma = st.sidebar.number_input('Population Standard Deviation (σ)', value=0.5, step=0.1)
sample_size = st.sidebar.number_input('Sample Size (n)', min_value=5, max_value=100, value=30)

# Role selection buttons
st.header("Select Your Role")
role_cols = st.columns(5)
roles = ['Storyteller', 'Sample Collector', 'Calculator', 'Judge', 'Decision Maker']
for idx, role_name in enumerate(roles):
    if role_cols[idx].button(role_name):
        st.session_state.role = role_name

# Display interfaces based on the selected role
if st.session_state.role == 'Storyteller':
    st.subheader("Storyteller: Setting the Scenario")
    st.write("""
        Welcome! Café Brew claims their coffee is ready in 2 minutes.  
        Your job is to use sample data and statistics to test this claim under busy conditions.
        Let's start by deciding how to gather and analyze the data.
    """)

elif st.session_state.role == 'Sample Collector':
    st.subheader("Sample Collector: Generate Sample Data")
    if st.button("Generate Sample Data Now"):
        st.session_state.sample_data = np.random.normal(mu_0, sigma, sample_size)
        st.write("Sample data generated and stored.")
    if st.session_state.sample_data is not None:
        st.write("Latest Sample Data:")
        st.write(st.session_state.sample_data)

elif st.session_state.role == 'Calculator':
    st.subheader("Calculator: Compute Sample Mean, SE, and Z-Score")
    if st.session_state.sample_data is None:
        st.write("Please generate sample data first (Sample Collector role).")
    else:
        sample_mean = np.mean(st.session_state.sample_data)
        se = sigma / np.sqrt(len(st.session_state.sample_data))
        z_score = (sample_mean - mu_0) / se

        st.write(f"Sample Mean (μ): {sample_mean:.3f}")
        st.write(f"Standard Error (SE): {se:.3f}")
        st.write(f"Z-Score: {z_score:.3f}")

        # Store for use by other roles
        st.session_state.sample_mean = sample_mean
        st.session_state.se = se
        st.session_state.z_score = z_score

elif st.session_state.role == 'Judge':
    st.subheader("Judge: Set Significance Level and Critical Value")
    alpha = st.slider("Select Significance Level (α)", 0.01, 0.1, value=st.session_state.alpha, step=0.01)
    critical_value = stats.norm.ppf(1 - alpha / 2)
    st.write(f"For α = {alpha}, the critical Z-value is ±{critical_value:.3f}")

    # Save to session state for other roles
    st.session_state.alpha = alpha
    st.session_state.critical_value = critical_value

elif st.session_state.role == 'Decision Maker':
    st.subheader("Decision Maker: Visualize and Conclude")
    if st.session_state.z_score is None:
        st.write("Please complete the calculation step first.")
    elif st.session_state.critical_value is None:
        st.write("Please set the significance level in the Judge role first.")
    else:
        z = st.session_state.z_score
        cv = st.session_state.critical_value
        decision = 'Reject the Null Hypothesis (H₀)' if abs(z) > cv else 'Fail to Reject the Null Hypothesis (H₀)'

        st.write(f"Z-Score: {z:.3f}")
        st.write(f"Critical Value: ±{cv:.3f}")
        st.write(f"Final Decision: {decision}")

        # Plot the Z-distribution with critical regions and Z-score mark
        x = np.linspace(-4, 4, 1000)
        y = stats.norm.pdf(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, label="Standard Normal Distribution")
        ax.fill_between(x, 0, y, where=(x <= -cv), color='red', alpha=0.3, label='Rejection Region')
        ax.fill_between(x, 0, y, where=(x >= cv), color='red', alpha=0.3)
        ax.axvline(z, color='blue', linestyle='--', label=f'Z = {z:.2f}')
        ax.legend()
        ax.set_xlabel('Z-Score')
        ax.set_ylabel('Probability Density')
        ax.set_title('Z-Test Standard Normal Distribution')
        st.pyplot(fig)

else:
    st.write("Please select a role above to begin the simulation.")