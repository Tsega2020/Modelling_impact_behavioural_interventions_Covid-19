######### Figure 3: Models used in the study
########## Python code to creat a word clound 
# Import necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Load the dataset
data = pd.read_excel("/kaggle/input/406-data-aug-01/406_DataEtraction_withRiskofBias_August_01_Final.xlsx")
df = pd.DataFrame(data)

# Filter the dataset based on 'Overall' column
filtered_df = df[df['Overall'] != 3].copy()

# Use the filtered_df DataFrame to count the word counts
Model_counts = filtered_df['6_Model Name'].value_counts()

# Convert the Series to a dictionary
Model_dict = Model_counts.to_dict()

# Generate the word cloud with adjusted parameters
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white', 
    max_words=100,  # Limit the number of words
    max_font_size=150,  # Increase maximum font size
    relative_scaling=0.5,  # Adjust relative scaling factor
    normalize_plurals=False  # Keep plural words distinct
).generate_from_frequencies(Model_dict)

# Display the word cloud
plt.figure(figsize=(12, 8))

# Plot the word cloud
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

# Get the top 5 counts
top_n = 3
top_counts_model = Model_counts.head(top_n)

# Add the top counts as a legend on the top right outside the plotting area
#legend_text_model = "\n".join([f"{model}: {count}" for model, count in top_counts_model.items()])
# Draw the box around the legend
#box_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")

#plt.text(0.78, 0.73, legend_text_model, fontsize=12, va='top', ha='left', 
 #        transform=plt.gcf().transFigure, bbox=box_props)

# Add title "Top Five" above the box
#plt.text(0.77, 0.74, "Top Three", fontsize=14, va='bottom', ha='left', 
 #        transform=plt.gcf().transFigure, fontweight='bold')

# Ensure space for the legend
plt.subplots_adjust(right=0.75)

# Save the plot
plt.savefig("/kaggle/working/Model_used_frequency_Nov03.tif", bbox_inches='tight')

# Show the plot
plt.show()
