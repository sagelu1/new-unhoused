import streamlit as st
import pandas as pd
import subprocess
import matplotlib.pyplot as plt

from plot_simulation import (
    make_assets_figure,
    make_homeless_figure,
    make_disability_figure,
    make_jobtraining_figure,
)

NUM_AGENTS = 10
MONTHS = 12

st.title("GCS Unhoused Model")
st.write(
    "Adjust the parameters for each agent, then click **Run Simulation** "
    "to update the model and plots."
)

# --- Agent sliders ---
agent_data = []
for i in range(NUM_AGENTS):
    st.subheader(f"Agent {i+1}")

    # Assets as an integer slider
    assets = st.slider(
        f"Assets (Agent {i+1})",
        min_value=0,
        max_value=40,      # tweak as you like
        value=10,
        step=1,
        key=f"assets_{i}",
    )

    # Disability
    disability = st.checkbox(
        "Disability",
        value=False,
        key=f"disability_{i}",
    )

    # Job Training
    job_training = st.checkbox(
        "Job Training",
        value=False,
        key=f"jobtraining_{i}",
    )

    # Homeless flag
    homeless = st.checkbox(
        "Initially Homeless",
        value=False,
        key=f"homeless_{i}",
    )

    # Ever Homeless flag
    ever_homeless = st.checkbox(
        "Ever Homeless Before",
        value=False,
        key=f"everhomeless_{i}",
    )

    # This tuple lines up exactly with agent_input.txt:
    # asset, disability, jobTraining, homeless, everHomeless
    agent_data.append((assets, disability, job_training, homeless, ever_homeless))


def write_agent_input_file(agent_rows):
    """
    Write agent_input.txt in the exact format Main.java expects:

    each
    asset,disability,jobTraining,homeless,everHomeless
    ...
    """
    with open("agent_input.txt", "w") as f:
        f.write("each\n")
        for assets, disability, job_training, homeless, ever_homeless in agent_rows:
            line = "{},{},{},{},{}\n".format(
                assets,
                str(disability).lower(),
                str(job_training).lower(),
                str(homeless).lower(),
                str(ever_homeless).lower(),
            )
            f.write(line)


def run_java_simulation():
    """
    Compile and run the Java simulation (Main.java, Agent.java, Home.java).
    Returns (ok: bool, error_message: str).
    """
    # 1) Compile
    try:
        compile_proc = subprocess.run(
            ["javac", "Main.java", "Agent.java", "Home.java"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return False, (
            "Could not find `javac`. Make sure Java JDK is installed "
            "and available on your PATH."
        )
    except subprocess.CalledProcessError as e:
        return False, f"Error compiling Java code:\n{e.stderr}"

    # 2) Run Main
    try:
        run_proc = subprocess.run(
            ["java", "Main"],
            check=True,
            capture_output=True,
            text=True,
        )
        # If Main writes to stdout/stderr you can inspect run_proc.stdout
    except FileNotFoundError:
        return False, (
            "Could not find `java`. Make sure Java is installed "
            "and available on your PATH."
        )
    except subprocess.CalledProcessError as e:
        return False, f"Error running Java simulation:\n{e.stderr}"

    return True, ""


st.markdown("---")

if st.button("Run Simulation"):
    # 1. Write the agent_input.txt based on slider values
    write_agent_input_file(agent_data)

    # 2. Run the Java simulation to regenerate the CSVs
    ok, msg = run_java_simulation()
    if not ok:
        st.error(msg)
    else:
        st.success("Simulation completed successfully! Updated CSV files generated.")

        # 3. Show plots using the newly generated CSVs
        st.subheader("Agent Asset Values Over Time")
        st.pyplot(make_assets_figure())

        st.subheader("Total Number of Homeless Agents Per Month")
        st.pyplot(make_homeless_figure())

        st.subheader("Total Disabled Agents Per Month")
        st.pyplot(make_disability_figure())

        st.subheader("Total Agents with Job Training Per Month")
        st.pyplot(make_jobtraining_figure())

        # (Optional) Show raw tables
        with st.expander("Show raw CSV data"):
            assets_df = pd.read_csv("assets.csv")
            homeless_df = pd.read_csv("homeless.csv")
            disability_df = pd.read_csv("disability.csv")
            jobtraining_df = pd.read_csv("jobtraining.csv")

            st.write("Assets")
            st.dataframe(assets_df)

            st.write("Homeless")
            st.dataframe(homeless_df)

            st.write("Disability")
            st.dataframe(disability_df)

            st.write("Job Training")
            st.dataframe(jobtraining_df)
