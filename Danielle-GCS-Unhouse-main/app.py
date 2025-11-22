import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import subprocess

NUM_AGENTS = 10
MONTHS = 12

# --- Agent sliders ---
agent_data = []
for i in range(NUM_AGENTS):
    st.subheader(f"Agent {i+1}")

    assets = st.slider(
        f"Assets (Agent {i+1})",
        min_value=0,
        max_value=100,
        value=10,
        step=1,
        key=f"assets_{i}",
    )

    disability = st.checkbox(
        "Disabled",
        value=False,
        key=f"disability_{i}",
    )

    job_training = st.checkbox(
        "Job Training",
        value=False,
        key=f"jobtraining_{i}",
    )

    homeless = st.checkbox(
        "Initially Homeless",
        value=False,
        key=f"homeless_{i}",
    )

    ever_homeless = st.checkbox(
        "Ever Homeless Before",
        value=False,
        key=f"everhomeless_{i}",
    )

    # This tuple lines up exactly with agent_input.txt:
    # asset, disability, jobTraining, homeless, everHomeless
    agent_data.append((assets, disability, job_training, homeless, ever_homeless))
