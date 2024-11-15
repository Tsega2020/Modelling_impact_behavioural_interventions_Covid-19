########### Figure 4: Percentage of Risk of Bias Assessment Across 15 Dimensions
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
#data = pd.read_csv("/kaggle/input/270-rob-csv-nov08-corr/270_ROB_csv_Nov08_cor.csv")
data = pd.read_excel("/kaggle/input/nov12rob-corr/270ROBexcel_Nov11cor.xlsx")
df = pd.DataFrame(data)

# Define risk colors based on the provided image, excluding "Critical"
risk_colors = {
    "Low": "#00A651",       # Green
    "Moderate": "yellow",   # Yellow
    "High": "#8B0000",      # Dark Red
    "Unclear": "grey",      # Grey
}

# Define the dimensions (columns) for the plot, skipping the 'Study ID'
dimensions = df.columns[1:]

# Reorder dimensions to have "Overall" at the end
dimensions = [dim for dim in dimensions if dim != "Overall"] + ["Overall"]
dimensions.reverse()  # Reverse the order to plot "Overall" at the bottom

# Calculate the counts and then percentages of each risk level per dimension
risk_counts = df.apply(lambda col: col.value_counts(normalize=True) * 100, axis=0).fillna(0)

# Reorder the index of risk_counts to match dimensions order
risk_counts = risk_counts[dimensions]

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Plot each risk level as a separate stacked bar
bottom = None
for risk_level, color in risk_colors.items():
    counts = risk_counts.loc[risk_level] if risk_level in risk_counts.index else [0] * len(dimensions)
    ax.barh(dimensions, counts, label=risk_level, left=bottom, color=color)
    if bottom is None:
        bottom = counts
    else:
        bottom += counts

# Add legend and labels
ax.set_xlabel('Percentage of Studies (%)',fontsize=12)
# ax.set_ylabel('Dimensions')
# ax.set_title('Risk of Bias Assessment Across 15 Dimensions')

# Position legend at the bottom
ax.legend(title='Risk Level', loc='upper center', fontsize=12, bbox_to_anchor=(0.5, -0.1), ncol=4)

# Increase fontsize of the dimension names
plt.yticks(fontsize=12)

# Adding custom text for vertical alignment
plt.text(-0.5, 0.35, 'Dimensions', horizontalalignment='right', verticalalignment='center', 
         rotation=90, fontsize=14, transform=ax.transAxes, bbox=dict(facecolor='white', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'))

plt.tight_layout()

# Save the figure
plt.savefig("Figure4_ROB_summary_plot.tif", bbox_inches='tight')

# Show the plot
plt.show()
