## Figure 5: Percentage of Risk Levels for Overall Risk of Bias

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Load the dataset
data = pd.read_excel("/kaggle/input/nov12rob-corr/270ROBexcel_Nov11cor.xlsx")
df = pd.DataFrame(data)

# Extract the "Overall" column
Overall_counts = df["Overall"].value_counts(normalize=True) * 100
print(Overall_counts)

# Define risk colors
risk_colors = {
    "Low": "#00A651",       # Green
    "Moderate": "yellow",   # Yellow
    "High": "#8B0000",      # Dark Red
    "Unclear": "grey",      # Grey
}

# Plotting the percentages for "Overall"
fig, ax = plt.subplots(figsize=(8, 7))

# Plot a bar chart
Overall_counts.plot(kind='bar', color=[risk_colors.get(level, "black") for level in Overall_counts.index], ax=ax,fontsize=13)

# Add labels and title
ax.set_ylabel('Percentage of Studies (%)',fontsize=13)
ax.set_xlabel('Risk Levels',fontsize=13)
ax.set_xticklabels(Overall_counts.index, rotation=0, ha='center', fontsize=13)
ax.set_title('Percentage of Risk Levels for Overall',fontsize=13)

# Manually create a legend
legend_elements = [Patch(facecolor=risk_colors[level], label=level) for level in Overall_counts.index]
ax.legend(handles=legend_elements, title='Risk Level', fontsize=13, bbox_to_anchor=(1.05, 1), loc='upper left')
# ax.legend(handles=legend_elements, title='Percentage of Risk Levels for Reporting Bias', bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the values on top of the bars
for i, (value, color) in enumerate(zip(Overall_counts, [risk_colors.get(level, "black") for level in Overall_counts.index])):
    ax.text(i, value + 1, f'{value:.1f}%', ha='center', color="black",fontsize=13)
plt.savefig('Figure5_Overall_risk_percentage.tif', bbox_inches='tight')
# Display the plot
plt.tight_layout()
plt.show()
