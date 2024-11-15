############### Code for Figure 14 Box plot of R0 by continent 
######### side by side the original and filtered (Low ROB) data frame. 
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress the FutureWarning related to pandas groupby
warnings.filterwarnings("ignore", category=FutureWarning, module="seaborn")

# Load the dataset
data = pd.read_excel("/kaggle/input/aug-03-406-data/406_DataEtraction_withRiskofBias_August_01_Final.xlsx")
df = pd.DataFrame(data)

# Filter the dataset based on 'Overall' column
filtered_df = df[df['Overall'] == 1].copy()

# Remove '>' and '<' signs but keep the numbers
df['14_R0_Basic Reproduction Number(R0)'] = df['14_R0_Basic Reproduction Number(R0)'].astype(str).replace({'<': '', '>': ''}, regex=True)
filtered_df['14_R0_Basic Reproduction Number(R0)'] = filtered_df['14_R0_Basic Reproduction Number(R0)'].astype(str).replace({'<': '', '>': ''}, regex=True)

# Convert '14_R0_Basic Reproduction Number(R0)' to numeric
df['14_R0_Basic Reproduction Number(R0)'] = pd.to_numeric(df['14_R0_Basic Reproduction Number(R0)'], errors='coerce')
filtered_df['14_R0_Basic Reproduction Number(R0)'] = pd.to_numeric(filtered_df['14_R0_Basic Reproduction Number(R0)'], errors='coerce')

# Define the order of continents, ensuring 'Worldwide' is at the end
continent_order = df['Continent'].dropna().unique().tolist()
if 'Worldwide' in continent_order:
    continent_order.remove('Worldwide')
continent_order.append('Worldwide')

# Ensure 'Continent' is a categorical type with the specified order
df['Continent'] = pd.Categorical(df['Continent'], categories=continent_order, ordered=True)
filtered_df['Continent'] = pd.Categorical(filtered_df['Continent'], categories=continent_order, ordered=True)

# Define a consistent color palette based on the order of continents
palette = sns.color_palette("husl", len(continent_order))
continent_palette = dict(zip(continent_order, palette))

# Plot for the original dataframe across continents
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
sns.boxplot(x='Continent', y='14_R0_Basic Reproduction Number(R0)', data=df, palette=continent_palette, order=continent_order)
plt.title('Box Plot of R0 in Original Data Across Continents')
plt.ylabel('Basic Reproduction Number (R0)')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

# Plot for the filtered dataframe across continents
plt.subplot(1, 2, 2)
sns.boxplot(x='Continent', y='14_R0_Basic Reproduction Number(R0)', data=filtered_df, palette=continent_palette, order=continent_order)
plt.title('Box Plot of R0 with Only Low Risk of Bias Studies Across Continents')
plt.ylabel('Basic Reproduction Number (R0)')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility

# Adding a common legend
plt.figlegend(handles=[plt.Line2D([0], [0], color=continent_palette[cont], lw=4) for cont in continent_order],
              labels=continent_order, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=len(continent_order), frameon=False)
plt.savefig("/kaggle/working/Figure14_boxplot_continent_original_filtered.tif", bbox_inches='tight')
plt.tight_layout()
plt.show()
