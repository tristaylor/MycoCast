import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define default environmental conditions
default_environment = {
    "temperature": 25,
    "co2": 400,
    "moisture": 40,
    "fragmentation": "high",
    "carbon_transfer_efficiency": 1.0
}

# Define remediation strategies
remediation_strategies = {
    "biochar": {"moisture": 5, "carbon_transfer_efficiency": 0.1},
    "inoculation": {"AMF_abundance": 10, "GRSP_concentration": 5},
    "compost": {"moisture": 3, "GRSP_concentration": 2},
    "humic substances": {"carbon_transfer_efficiency": 0.2, "moisture": 4}
}

# User input for environmental conditions
st.title("Mycorrhizal Health Simulator")
st.sidebar.header("Set Environmental Conditions")

environment = {key: st.sidebar.slider(f"{key}", min_value=0, max_value=100, value=default_environment[key]) 
               for key in default_environment if isinstance(default_environment[key], (int, float))}

# Function to simulate fungal health
def simulate_health(environment, remediation=None):
    health = np.random.uniform(0.5, 1.0)  # Initial fungal health
    
    # Apply environmental stress
    if environment["moisture"] < 30:
        health *= 0.9
    if environment["fragmentation"] == "high":
        health *= 0.85
    
    # Apply remediation if selected
    if remediation:
        for key, value in remediation.items():
            if key in environment:
                environment[key] += value
        health *= 1.1  # Simulated remediation benefit

    return max(0, min(health, 1))

# Show baseline fungal health
baseline_health = simulate_health(environment)
st.write(f"Baseline Mycorrhizal Health: **{baseline_health:.2f}**")

# User selects a remediation strategy
remediation_choice = st.selectbox("Choose a Remediation Strategy", list(remediation_strategies.keys()))
remediated_health = simulate_health(environment, remediation_strategies[remediation_choice])

# Compare results
st.write(f"**After Applying {remediation_choice}: {remediated_health:.2f}**")

# Plot results
fig, ax = plt.subplots()
ax.bar(["Baseline", remediation_choice], [baseline_health, remediated_health], color=["#FFDDDD", "#C3E6CB"])
ax.set_ylabel("Fungal Health")
ax.set_title("Effect of Remediation Strategies")
st.pyplot(fig)
