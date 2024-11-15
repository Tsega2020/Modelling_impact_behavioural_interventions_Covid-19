# Python Code for Figure 7 boxplot by continent.
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.patches as mpatches

# Load the dataset
data = pd.read_excel("/kaggle/input/nov11-excel-406-dataextracted/TKG_CJA_Extracted_Data_406_270_Nov_11.xlsx")
#data = pd.read_excel("")
df = pd.DataFrame(data)

# Filter the dataset based on 'Overall' column
filtered_df = df[df['Overall'] != 3].copy()

# Remove '>' and '<' signs but keep the numbers
df['15_R0_Basic Reproduction Number(R0)'] = df['15_R0_Basic Reproduction Number(R0)'].astype(str).replace({'<': '', '>': ''}, regex=True)
filtered_df['15_R0_Basic Reproduction Number(R0)'] = filtered_df['15_R0_Basic Reproduction Number(R0)'].astype(str).replace({'<': '', '>': ''}, regex=True)

# Convert '14_R0_Basic Reproduction Number(R0)' to numeric, forcing errors to NaN
df['15_R0_Basic Reproduction Number(R0)'] = pd.to_numeric(df['15_R0_Basic Reproduction Number(R0)'], errors='coerce')
filtered_df['15_R0_Basic Reproduction Number(R0)'] = pd.to_numeric(filtered_df['15_R0_Basic Reproduction Number(R0)'], errors='coerce')

# Drop rows with NaN values in '14_R0_Basic Reproduction Number(R0)' column
filtered_df = filtered_df.dropna(subset=['15_R0_Basic Reproduction Number(R0)'])

# Define the order of the continents with "Worldwide" at the end
unique_continents = list(filtered_df['6_Continent'].unique())
unique_continents.remove("Worldwide")
unique_continents.append("Worldwide")

# Calculate sample sizes for each continent and the Q3 values
continent_counts = filtered_df['6_Continent'].value_counts().reindex(unique_continents)
q3_values = filtered_df.groupby('6_Continent')['15_R0_Basic Reproduction Number(R0)'].quantile(0.75).reindex(unique_continents)

# Create the box plot for '14_R0_Basic Reproduction Number(R0)'
plt.figure(figsize=(10, 6))
boxplot = sns.boxplot(x='6_Continent', y='15_R0_Basic Reproduction Number(R0)', data=filtered_df, 
                      palette='Set3', order=unique_continents)

# Set the x-label and adjust its position
ax = plt.gca()
ax.set_xlabel('Continent', fontsize=12)
ax.xaxis.set_label_coords(0.5, -0.1)  # Set the x-label position
plt.ylabel('R0', fontsize=12)
plt.title('R0 by Continent')
plt.grid(True)
plt.tight_layout()

# Set transparency for the boxes
for patch in boxplot.artists:
    r, g, b, _ = patch.get_facecolor()
    patch.set_facecolor((r, g, b, 0.8))  # Set the alpha value here

# Add sample size annotations above the 75% quartile (Q3) for each continent
for i, (continent, count) in enumerate(continent_counts.items()):
    q3_value = q3_values[continent] if not pd.isna(q3_values[continent]) else 0
    plt.text(i-0.17, q3_value + 1.5, f'n={count}', ha='center', va='bottom', fontsize=10, color='black')

# Create a legend
handles = []
colors = sns.color_palette('Set3', len(unique_continents))

for Continent, color in zip(unique_continents, colors):
    handles.append(mpatches.Patch(color=color, label=Continent))

plt.legend(handles=handles, title='Continent', loc='upper right')

# Save the plot
plt.savefig("/kaggle/working/Figure7_box_plot_by_continentNov11.tif", bbox_inches='tight')
plt.show()
