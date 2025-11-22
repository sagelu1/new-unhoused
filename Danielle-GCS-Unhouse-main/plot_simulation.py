import pandas as pd
import matplotlib.pyplot as plt

# --- Assets plot ---
assets_df = pd.read_csv("assets.csv")
months = assets_df['Month']

plt.figure(figsize=(10,6))
for agent in assets_df.columns[1:]:  # skip 'Month'
    plt.plot(months, assets_df[agent], marker='o', label=agent)

plt.xlabel("Month")
plt.ylabel("Asset Value")
plt.title("Agent Asset Values Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Homeless plot ---
homeless_df = pd.read_csv("homeless.csv")
plt.figure(figsize=(10,6))

# Convert all agent columns to integers (in case they were strings)
agent_cols = homeless_df.columns[1:]
homeless_df[agent_cols] = homeless_df[agent_cols].astype(int)

# Sum across all agent columns for each month
homeless_totals = homeless_df[agent_cols].sum(axis=1)

plt.bar(homeless_df['Month'], homeless_totals, color='skyblue')
plt.xlabel("Month")
plt.ylabel("Total Homeless Agents")
plt.title("Total Homeless Agents Per Month")
plt.ylim(0, 10)  # explicitly set Y-axis
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# --- Disability plot ---
disability_df = pd.read_csv("disability.csv")
plt.figure(figsize=(10,6))
plt.bar(disability_df['Month'], disability_df['Disability_Total'], color='orange')
plt.xlabel("Month")
plt.ylabel("Total Disabled Agents")
plt.title("Total Disabled Agents Per Month")
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# --- Job Training plot ---
jobtraining_df = pd.read_csv("jobtraining.csv")
plt.figure(figsize=(10,6))

jobtraining_df['JobTraining_Total'] = jobtraining_df['JobTraining_Total'].astype(int)

plt.bar(jobtraining_df['Month'], jobtraining_df['JobTraining_Total'], color='green')
plt.xlabel("Month")
plt.ylabel("Total Agents with Job Training")
plt.title("Total Agents with Job Training Per Month")
plt.ylim(0, 10)  # explicitly set Y-axis
plt.grid(axis='y')
plt.tight_layout()
plt.show()
