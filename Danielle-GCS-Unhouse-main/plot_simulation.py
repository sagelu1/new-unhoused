import pandas as pd
import matplotlib.pyplot as plt


def make_assets_figure():
    assets_df = pd.read_csv("assets.csv")
    months = assets_df["Month"]

    fig, ax = plt.subplots(figsize=(10, 6))
    for agent in assets_df.columns[1:]:  # skip 'Month'
        ax.plot(months, assets_df[agent], marker="o", label=agent)

    ax.set_xlabel("Month")
    ax.set_ylabel("Asset Value")
    ax.set_title("Agent Asset Values Over Time")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig


def make_homeless_figure():
    homeless_df = pd.read_csv("homeless.csv")

    # Convert all agent columns to integers
    agent_cols = homeless_df.columns[1:]
    homeless_df[agent_cols] = homeless_df[agent_cols].astype(int)

    # Sum across all agent columns for each month
    homeless_totals = homeless_df[agent_cols].sum(axis=1)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(homeless_df["Month"], homeless_totals)
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Homeless Agents")
    ax.set_title("Total Number of Homeless Agents Per Month")
    ax.grid(axis="y")
    fig.tight_layout()
    return fig


def make_disability_figure():
    disability_df = pd.read_csv("disability.csv")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(disability_df["Month"], disability_df["Disability_Total"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Disabled Agents")
    ax.set_title("Total Disabled Agents Per Month")
    ax.grid(axis="y")
    fig.tight_layout()
    return fig


def make_jobtraining_figure():
    jobtraining_df = pd.read_csv("jobtraining.csv")
    jobtraining_df["JobTraining_Total"] = jobtraining_df["JobTraining_Total"].astype(
        int
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(jobtraining_df["Month"], jobtraining_df["JobTraining_Total"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Agents with Job Training")
    ax.set_title("Total Agents with Job Training Per Month")
    ax.set_ylim(0, 10)  # tweak based on your agent count
    ax.grid(axis="y")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    # Optional: if you run this file directly, show the plots one after another
    make_assets_figure()
    plt.show()

    make_homeless_figure()
    plt.show()

    make_disability_figure()
    plt.show()

    make_jobtraining_figure()
    plt.show()

