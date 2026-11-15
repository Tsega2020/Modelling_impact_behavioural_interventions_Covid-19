# For Figure 6 and Supporting information (S1_Fig15, S2_Fig16, S3_Fig17)
# Code for risk of bias assessment using functions
# Function to sort and plot by risk level order 
# Function to sort and plot by ID order
# Function for Figure 6: Side-by-side plot of Chunk 1 and Chunk 6 
# Function for S1_Fig15_Reportingbias: Percentage of Risk Levels for Reporting Bias 
# Function for S2_Fig16_RoB-Chunk_1_2_3: Side-by-side plot of Chunks 1, 2, and 3 
# Function for S3_Fig17_RoB-Chunk-4_5_6: Side-by-side plot of Chunks 4, 5, and 6
# Existing imports and setup

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Patch
from PIL import Image

# Load the dataset
def load_data(filepath):
    data = pd.read_excel(filepath)
    df = pd.DataFrame(data)
    return df

# Mapping categories to numerical values and symbols
category_map = {
    'Low': (1, '+', '#32CD32'), # green
    'Moderate': (0, '-', '#FFEB3B'), # yellow
    'High': (-1, 'x', '#A83232'), # red
    'Unclear': (np.nan, '?', 'lightgrey') # lightgrey
}

# Function to draw circles with symbols
def draw_circle(ax, x, y, symbol, color):
    circle = Circle((x, y), 0.3, color=color, fill=True)
    ax.add_patch(circle)
    ax.text(x, y, symbol, color='black', fontsize=10, ha='center', va='center')

# Function to prepare data for plotting
def prepare_data(df):
    numeric_data = np.zeros(df.iloc[:, 1:].shape)
    symbol_data = np.empty(df.iloc[:, 1:].shape, dtype=object)
    color_data = np.empty(df.iloc[:, 1:].shape, dtype=object)

    for i, (idx, row) in enumerate(df.iterrows()):
        for j, item in enumerate(row[1:]):  # Skip the first column 'Study ID'
            num_val, symbol, color = category_map[item]
            numeric_data[i, j] = num_val
            symbol_data[i, j] = symbol
            color_data[i, j] = color

    return numeric_data, symbol_data, color_data

# Function to plot chunks
def plot_chunks(chunks, symbol_chunks, color_chunks, id_chunks, dimension_descriptions, filename_prefix):
    for i, (chunk, sym_chunk, col_chunk, id_chunk) in enumerate(zip(chunks, symbol_chunks, color_chunks, id_chunks)):
        fig, ax = plt.subplots(figsize=(12, 18))  # Adjusted figure size for better clarity

        # Draw labels as part of the grid
        for col in range(chunk.shape[1] + 1):
            if col == 0:
                ax.text(col, 0, '', va='center', ha='center', fontsize=12, bbox=dict(facecolor='lightgrey', edgecolor='lightgrey'))
            else:
                ax.text(col, 0, f'D{col}', va='center', ha='center', fontsize=12)

        for row in range(chunk.shape[0] + 1):
            if row == 0:
                ax.text(0, row, '', va='center', ha='center', fontsize=12)
            else:
                ax.text(0, row, f"E_{id_chunk.iloc[row-1]}", va='center', ha='center', fontsize=12)  # Display sorted study IDs

        # Shading the row and column labels
        ax.add_patch(Rectangle((-0.5, -0.5), 1, chunk.shape[0]+1, color='lightgrey', lw=0))  # Left label shading
        ax.add_patch(Rectangle((-0.5, -0.5), chunk.shape[1], 1, color='lightgrey', lw=0))  # Top label shading
        ax.add_patch(Rectangle((chunk.shape[1]-0.5, -0.5), 1, chunk.shape[0]+1, color='lightgrey', lw=0))  # Right label shading

        # Display the data, starting from (1,1) to leave (0,0) for labels
        for row in range(chunk.shape[0]):
            for col in range(chunk.shape[1]):
                symbol = sym_chunk[row, col]
                color = col_chunk[row, col]
                draw_circle(ax, col + 1, row + 1, symbol, color)

        # Adjust axes limits
        ax.set_xlim(-0.5, chunk.shape[1] + 0.5)
        ax.set_ylim(chunk.shape[0] + 0.5, -0.5)

        # Add gridlines between circles
        ax.set_xticks(np.arange(-0.5, chunk.shape[1] + 0.5, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, chunk.shape[0] + 0.5, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.15)
        
        # Remove major ticks
        ax.set_xticks([])
        ax.set_yticks([])

        # Add the legend below the plot to the right
        legend_elements = [
            Circle((0, 0), 0.03, color='#32CD32', fill=True, label='Low'), # green 
            Circle((0, 0), 0.03, color='#FFEB3B', fill=True, label='Moderate'), # yellow
            Circle((0, 0), 0.03, color='#A83232', fill=True, label='High'),  # red 
            Circle((0, 0), 0.03, color='lightgrey', fill=True, label='Unclear')
        ]       
            
        legend = ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.8, -0.016), 
                           ncol=1, fontsize=12, frameon=False, title="Judgement")
        legend.set_title("Judgement", prop={'size': 12})
        
        # Dimension descriptions at the bottom left
        plt.figtext(0.13, -0.091, "\n".join(dimension_descriptions), fontsize=12, va='bottom', ha='left')

        # Titles and labels
        fig.text(0.09, 0.4, 'Study', va='center', rotation='vertical', fontsize=13)
        fig.suptitle('Risk of Bias', fontsize=12, y=0.89)

        # Save each chunk as a separate figure
        plt.savefig(f'{filename_prefix}_Chunk_{i+1}.tif', bbox_inches='tight')
        plt.show()

# Function to sort and plot by risk level
def sort_and_plot_by_risk_level(df, dimension_descriptions):
    # Extracting the study IDs
    study_ids = df.iloc[:, 0].apply(lambda x: int(x.split('_')[1]))  

    numeric_data, symbol_data, color_data = prepare_data(df)

    # Count the number of 'High', 'Low', 'Moderate', and 'Unclear' judgments
    high_counts = (numeric_data == -1).sum(axis=1)
    low_counts = (numeric_data == 1).sum(axis=1)
    moderate_counts = (numeric_data == 0).sum(axis=1)
    unclear_counts = np.isnan(numeric_data).sum(axis=1)

    # Sorting order by risk levels
    sorted_indices = np.lexsort((study_ids, unclear_counts, -moderate_counts, -low_counts, high_counts))

    # Sort the data
    numeric_data = numeric_data[sorted_indices]
    symbol_data = symbol_data[sorted_indices]
    color_data = color_data[sorted_indices]
    sorted_study_ids = study_ids.iloc[sorted_indices]

    # Define the study chunks
    chunk_ranges = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 235), (235, 270)]
    chunks = [numeric_data[start:end] for start, end in chunk_ranges]
    symbol_chunks = [symbol_data[start:end] for start, end in chunk_ranges]
    color_chunks = [color_data[start:end] for start, end in chunk_ranges]
    id_chunks = [sorted_study_ids[start:end] for start, end in chunk_ranges]

    plot_chunks(chunks, symbol_chunks, color_chunks, id_chunks, dimension_descriptions, 'RoB_Risk_Level')

# Function to sort and plot by ID order
def sort_and_plot_by_id(df, dimension_descriptions):
    numeric_data, symbol_data, color_data = prepare_data(df)

    # Define the study chunks
    chunk_ranges = [(0, 50), (50, 100), (100, 150), (150, 200), (200, 235), (235, 270)]
    chunks = [numeric_data[start:end] for start, end in chunk_ranges]
    symbol_chunks = [symbol_data[start:end] for start, end in chunk_ranges]
    color_chunks = [color_data[start:end] for start, end in chunk_ranges]
    id_chunks = [pd.Series(range(start+1, end+1)) for start, end in chunk_ranges]

    plot_chunks(chunks, symbol_chunks, color_chunks, id_chunks, dimension_descriptions, 'RoB_ID')

# Dimension descriptions
dimension_descriptions = [
    'Domains:',
    "D1: Research Question, Goals, and Scope",
    "D2: Model Structure and Assumptions",
    "D3: Definition and Justification of Model Components and Relationships",
    "D4: Data Informed Model",
    "D5: Reflection of Uncertainty",
    "D6: Sensitivity and Stability Analyses",
    "D7: Model Assessment",
    "D8: Transparency",
    "D9: Selection Bias",
    "D10: Performance Bias",
    "D11: Detection Bias",
    "D12: Attrition Bias",
    "D13: Reporting Bias",
    "D14: Confounding",
    "D15: External Validity",
    "D16: Overall"
]

# Function for Figure 6: Side-by-side plot of Chunk 1 and Chunk 6
def plot_side_by_side_chunks_1_6():
    Chunk1_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_1.tif")
    Chunk6_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_6.tif")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 30))
    ax1.imshow(Chunk1_image)
    ax1.axis('off')
    ax2.imshow(Chunk6_image)
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig('Figure6_RoB_85.tif', bbox_inches='tight')
    plt.show()

# Function for S1_Fig15_Reportingbias: Percentage of Risk Levels for Reporting Bias
def plot_reporting_bias(df):
    #data = pd.read_excel('/kaggle/input/nov-15-rob-fig6-s1-15-s2-16-s3-17/270ROBexcel_Nov11cor.xlsx')
    #df = pd.DataFrame(data)
    reporting_bias_counts = df["Reporting Bias"].value_counts(normalize=True) * 100
    
    risk_colors = {
        "Low": "#00A651",
        "Moderate": "yellow",
        "High": "#8B0000",
        "Unclear": "grey",
    }
    
    fig, ax = plt.subplots(figsize=(7, 5))
    reporting_bias_counts.plot(kind='bar', color=[risk_colors.get(level, "black") for level in reporting_bias_counts.index], ax=ax, fontsize=12)
    ax.set_ylabel('Percentage of Studies (%)', fontsize=12)
    ax.set_xlabel('Risk Levels', fontsize=12)
    ax.set_xticklabels(reporting_bias_counts.index, rotation=0, ha='center', fontsize=13)
    ax.set_title('Percentage of Risk Levels for Reporting Bias', fontsize=12)
    
    legend_elements = [Patch(facecolor=risk_colors[level], label=level) for level in reporting_bias_counts.index]
    ax.legend(handles=legend_elements, title='Risk Level', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    
    for i, value in enumerate(reporting_bias_counts):
        ax.text(i, value + 1, f'{value:.1f}%', ha='center', color="black", fontsize=12)
    
    plt.tight_layout()
    plt.savefig('S1_Fig15_Reportingbias.tif', bbox_inches='tight')
    plt.show()

# Function for S2_Fig16_RoB-Chunk_1_2_3: Side-by-side plot of Chunks 1, 2, and 3
def plot_side_by_side_chunks_1_2_3():
    Chunk1_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_1.tif")
    Chunk2_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_2.tif")
    Chunk3_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_3.tif")
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 30))
    ax1.imshow(Chunk1_image)
    ax1.axis('off')
    ax2.imshow(Chunk2_image)
    ax2.axis('off')
    ax3.imshow(Chunk3_image)
    ax3.axis('off')
    
    plt.tight_layout()
    plt.savefig('S2_Fig16_RoB-Chunk_1_2_3.tif', bbox_inches='tight')
    plt.show()

# Function for S3_Fig17_RoB-Chunk-4_5_6: Side-by-side plot of Chunks 4, 5, and 6
def plot_side_by_side_chunks_4_5_6():
    Chunk4_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_4.tif")
    Chunk5_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_5.tif")
    Chunk6_image = Image.open("/kaggle/working/RoB_Risk_Level_Chunk_6.tif")
    
    fig, (ax4, ax5, ax6) = plt.subplots(1, 3, figsize=(30, 30))
    ax4.imshow(Chunk4_image)
    ax4.axis('off')
    ax5.imshow(Chunk5_image)
    ax5.axis('off')
    ax6.imshow(Chunk6_image)
    ax6.axis('off')
    
    plt.tight_layout()
    plt.savefig('S3_Fig17_RoB-Chunk-4_5_6.tif', bbox_inches='tight')
    plt.show()

# Main function to run the analysis
def main():
    filepath = "/kaggle/input/nov-15-rob-fig6-s1-15-s2-16-s3-17/270ROBexcel_Nov11cor.xlsx"
    df = load_data(filepath)

    # Explanation before plotting by risk level
    print("""
    Generating figures sorted by risk levels...
    These figures show the risk of bias across studies, sorted primarily by the number of 'High', 'Moderate', 'Low', and 'Unclear' judgments.
    This sorting helps to visually prioritize studies with the most concerning levels of bias.
    """)

    # Call the function to sort and plot by risk level
    sort_and_plot_by_risk_level(df, dimension_descriptions)

    # Explanation before plotting by study ID
    #print("""
    #Generating figures sorted by study ID...
    #These figures display the risk of bias in the order of study IDs.
    #This sorting presents the data as it was originally ordered, allowing for a direct comparison of bias as recorded in the dataset.
    #""")

    # Call the function to sort and plot by ID order
    #sort_and_plot_by_id(df, dimension_descriptions)

    # Call the new functions for additional figures
    plot_side_by_side_chunks_1_6()
    plot_reporting_bias(df)
    plot_side_by_side_chunks_1_2_3()
    plot_side_by_side_chunks_4_5_6()

if __name__ == "__main__":
    main()
