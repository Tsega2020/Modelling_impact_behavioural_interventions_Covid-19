############## Figure 13 box plots for 'R0' in both original and filtered (Low ROB) dataframes
########
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_excel("/kaggle/input/aug-03-406-data/406_DataEtraction_withRiskofBias_August_01_Final.xlsx")
df = pd.DataFrame(data)

# Filter the dataset based on 'Overall' column
filtered_df = df[df['Overall'] == 1].copy()

# Remove '>' and '<' signs but keep the numbers
df['14_R0_Basic Reproduction Number(R0)'] = df['14_R0_Basic Reproduction Number(R0)'].astype(str).replace({'<': '', '>': ''}, regex=True)
filtered_df['14_R0_Basic Reproduction Number(R0)'] = filtered_df['14_R0_Basic Reproduction Number(R0)'].astype(str).replace({'<': '', '>': ''}, regex=True)

# Convert '14_R0_Basic Reproduction Number(R0)' to numeric, forcing errors to NaN
df['14_R0_Basic Reproduction Number(R0)'] = pd.to_numeric(df['14_R0_Basic Reproduction Number(R0)'], errors='coerce')
filtered_df['14_R0_Basic Reproduction Number(R0)'] = pd.to_numeric(filtered_df['14_R0_Basic Reproduction Number(R0)'], errors='coerce')

# Create box plots for 'R0' in both original and filtered dataframes
plt.figure(figsize=(10, 6))

# Prepare the data for box plot
data1 = df['14_R0_Basic Reproduction Number(R0)'].dropna()
data2 = filtered_df['14_R0_Basic Reproduction Number(R0)'].dropna()

# Create the box plot
box = plt.boxplot([data1, data2], labels=['All Studies (including high risk of bias)', 'Low Risk of Bias Studies Only'], patch_artist=True)
# Set custom labels with increased fontsize
plt.xticks([1, 2], ['All Studies (including high risk of bias)', 'Low Risk of Bias Studies Only'], fontsize=14)

# Set colors for the boxes
colors = ['blue', 'green']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Set labels and title
plt.ylabel('Basic Reproduction Number (R0)', fontsize=14)
plt.title('R0 of all 270 studies Vs R0 of only low risk studies', fontsize=14)

# Add a legend
plt.legend([plt.Line2D([0], [0], color=c, lw=3) for c in colors],
           ['All Studies \n (including high \n risk of bias)', 'Low Risk of Bias \n Studies Only'], loc='upper right')

# Save and show the plot
plt.tight_layout()
plt.savefig("/kaggle/working/Figure13_boxplot_Overall_original_filtered.tif", bbox_inches='tight')
plt.show()
