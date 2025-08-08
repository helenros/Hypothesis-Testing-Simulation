import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

st.title('Walk the Curve: Z-Test Hypothesis Testing Simulation')
st.write("""
           Welcome to the Walk the Curve simulation! This simulation immerses you in hypothesis testing through Café Brew’s 2-minute coffee service claim. Participants assume various roles—from defining hypotheses and gathering data to calculation and decision-making—using Z-test concepts. By interacting with real sample data, users learn to evaluate statistical evidence, interpret Z-scores, and understand significance levels. This hands-on experience demonstrates how statistical methods support operational business decisions, making abstract concepts accessible through a practical, engaging scenario.
        """)


# Initialize session state if not present
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

# Sidebar inputs
mu_0 = st.sidebar.number_input('Population Mean (μ₀)', value=2.0, step=0.1)
sigma = st.sidebar.number_input('Population Standard Deviation (σ)', value=0.5, step=0.1)
sample_size = st.sidebar.number_input('Sample Size (n)', min_value=5, max_value=100, value=30)

# Define roles with detailed 150-word explanations
roles = [
    {"name": "Storyteller", "color": "#FF6347", "icon": "📖", "desc": """
     Welcome to the Walk the Curve simulation! Café Brew, a rapidly expanding coffee retailer, recently launched an ambitious campaign promising customers that coffee will be served in under 2 minutes. This operational strategy targets busy customers seeking quick service without compromising quality. Before the campaign is implemented nationwide, the management tasked operations analyst Riya Sharma to validate this claim using statistical evidence.
"""},
    
    {"name": "Set Hypothesis", "color": "#B4EEF4", "icon": "🧮", "desc": """Set Hypothesis button reveals the fundamental hypotheses that frame the statistical test.

The Null Hypothesis (H₀) assumes that the average coffee preparation time is exactly 2 minutes, as claimed by Café Brew, implying no difference or change regardless of varying conditions.

The Alternative Hypothesis (H₁) posits that the actual average preparation time differs from 2 minutes, reflecting potential deviations during busy hours.

Clearly stating these hypotheses is crucial because it establishes the question the data aims to answer and directs the subsequent analysis. Defining both hypotheses provides a clear criterion for decision-making: evidence will either support rejecting or failing to reject the null hypothesis. This process underpins objective statistical reasoning, guides interpretation of test results, and ensures that conclusions are logically and scientifically grounded."""},
    
    {"name": "Sample Collector", "color": "#4682B4", "icon": "📊", "desc": "The Sample Collector’s task is to gather data representative of café coffee preparation times. By simulating or collecting data, you ensure randomness and reliability critical for valid inference. Your input serves as the foundation for all subsequent analysis, simulating how real-world researchers collect empirical evidence."},

    {"name": "Calculator", "color": "#32CD32", "icon": "🧮", "desc": "The Calculator processes the sample data to find summary statistics. This role walks step-by-step through formulas to compute the sample mean, standard error, and Z-score. By showing detailed calculations, you help make the abstract statistical concepts tangible and clear."},

    {"name": "Judge", "color": "#FFD700", "icon": "⚖️", "desc": "The Judge determines the significance level, or alpha, defining the threshold for evidence strength. Computing the critical Z-value, you specify the region where sample results are deemed statistically significant, balancing risk of false positives (Type I errors) against confidence."},

    {"name": "Decision Maker", "color": "#8A2BE2", "icon": "🧑‍⚖️", "desc": """
The Decision Maker evaluates the Z-score against the critical region to decide if the null hypothesis should be rejected or not. You visualize results graphically and interpret them in context, explaining implications for the café’s claim. Your explanation translates technical results into practical business insight, making the conclusion actionable.
"""}
]

button_width = "100px"
button_height = "100px"

st.header("Select Your Role")
cols = st.columns(len(roles))

for idx, role in enumerate(roles):
    # Custom button using HTML for background color and size
    # Button id for each role
    button_id = f"custom_btn_{idx}"
    html_button = f"""
    <style>
        #{button_id} {{
            background-color: {role['color']};
            color: black;
            font-weight: bold;
            font-size: 16px;
            height: {button_height};
            width: {button_width};
            border: 2px solid #eee;
            border-radius: 12px;
            cursor: pointer;
            text-align: Centre;
            margin-bottom: 0px;
            margin-top: 0px;
            transition: filter 0.2s;
        }}
        #{button_id}:hover {{
            filter: brightness(90%);
            border-color: #333;
        }}
    </style>
    <button id="{button_id}">{role['icon']} {role['name']}</button>
    """
    cols[idx].markdown(html_button, unsafe_allow_html=True)
    # Overlay native Streamlit button for click event
    # make sure it matches size visually (label empty so only the HTML button is visible)
    if cols[idx].button("👉", key=role['name'], help="Click"):
       st.session_state.role = role['name']





# Role-based UI and logic
if st.session_state.role:
    selected_role = next(r for r in roles if r["name"] == st.session_state.role)
    st.subheader(f"{selected_role['icon']} {selected_role['name']}")
    st.write(selected_role['desc'])

    if st.session_state.role == "Storyteller":
        st.write("""
          Riya collected preparation time data from a random sample of 30 coffee orders at a flagship outlet. The sample had an average preparation time of exactly 2 minutes with a standard deviation of 0.5 minutes. This data was compared against the historical average preparation time of 2 minutes.

          This simulation explores the process of statistically testing whether the café’s promise holds true during busy hours. Various roles collaborate to understand the data, perform calculations, set testing criteria, and make informed decisions. Each role plays a vital part in the journey from raw data to actionable business insights.
                          
          Ready to start the simulation? Step into the shoes of each role, from data collector to decision maker, and experience firsthand how businesses use statistics to support critical operational claims. Let’s walk the curve together—your journey to uncovering insights begins now!     
        """)

    elif st.session_state.role == "Set Hypothesis":
            st.markdown(f"**Null Hypothesis (H₀):** The mean coffee preparation time is {mu_0:.3f} minutes (μ = {mu_0:.3f}).")
            st.markdown(f"**Alternative Hypothesis (H₁):** The mean coffee preparation time is not {mu_0:.3f} minutes (μ ≠ {mu_0:.3f}).")

    elif st.session_state.role == "Sample Collector":
        if st.button("Generate Sample Data"):
            st.session_state.sample_data = np.random.normal(mu_0, sigma, sample_size)
            st.success("Sample data generated and stored.")
        if st.session_state.sample_data is not None:
            st.write("Sample data:")
            st.write(st.session_state.sample_data)

    elif st.session_state.role == "Calculator":
        if st.session_state.sample_data is None:
            st.warning("Please generate sample data first.")
        else:
            sample_mean = np.mean(st.session_state.sample_data)
            st.write(f"Sample Mean (x̄) = (Sum of all sample values) / n = {sample_mean:.3f}")

            se = sigma / np.sqrt(len(st.session_state.sample_data))
            st.write(f"Standard Error (SE) = σ / √n = {sigma:.3f} / √{len(st.session_state.sample_data)} = {se:.3f}")

            z_score = (sample_mean - mu_0) / se
            st.write(f"Z-Score = (x̄ - μ₀) / SE = ({sample_mean:.3f} - {mu_0:.3f}) / {se:.3f} = {z_score:.3f}")

            st.session_state.sample_mean = sample_mean
            st.session_state.se = se
            st.session_state.z_score = z_score

    elif st.session_state.role == "Judge":
        alpha = st.slider("Select Significance Level (α)", 0.01, 0.1, value=st.session_state.alpha, step=0.01)
        critical_value = stats.norm.ppf(1 - alpha / 2)
        st.write(f"For α = {alpha}, the Critical Z-value is ±{critical_value:.3f}")

        st.session_state.alpha = alpha
        st.session_state.critical_value = critical_value

    elif st.session_state.role == "Decision Maker":
        if st.session_state.z_score is None:
            st.warning("Please complete calculations first.")
        elif st.session_state.critical_value is None:
            st.warning("Please set the significance level first.")
        else:
            z = st.session_state.z_score
            cv = st.session_state.critical_value
            decision = "Reject the Null Hypothesis (H₀)" if abs(z) > cv else "Fail to Reject the Null Hypothesis (H₀)"
            st.write(f"Z-Score: {z:.3f}")
            st.write(f"Critical Value: ±{cv:.3f}")
            st.write(f"Decision: {decision}")

            if decision.startswith("Reject"):
                st.markdown(f"""
                **Explanation:** Since the Z-score lies outside the critical values, the evidence suggests that the average coffee preparation time differs significantly from {mu_0:.3f} minutes. This implies that Café Brew's claim may not hold during busy hours, possibly affecting customer satisfaction and business performance.
                """)
             
            else:
                st.markdown(f"""
                **Explanation:** The Z-score falls within the acceptance range, indicating insufficient evidence to dispute Café Brew's claim. The average preparation time during peak hours appears consistent with the promise of {mu_0:.3f} minutes, supporting the business’s marketing.
                """)

            x = np.linspace(-4, 4, 1000)
            y = stats.norm.pdf(x)

            fig, ax = plt.subplots()
            ax.plot(x, y, label="Standard Normal Distribution")
            ax.fill_between(x, 0, y, where=(x <= -cv), color="red", alpha=0.3, label="Rejection Region")
            ax.fill_between(x, 0, y, where=(x >= cv), color="red", alpha=0.3)
            ax.axvline(z, color="blue", linestyle="--", label=f"Z-score = {z:.2f}")

            ax.legend()
            ax.set_xlabel("Z-Score")
            ax.set_ylabel("Probability Density")
            ax.set_title("Z-Test Standard Normal Distribution")

            st.pyplot(fig)

else:
    st.write("Please select a role above to begin the simulation.")
