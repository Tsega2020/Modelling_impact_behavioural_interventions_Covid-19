#####################################
########### Figure 12-right panel: for Key findings
############# A word cloud for key findings column
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

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text)  # Remove punctuation
    text = text.lower()  # Lowercase
    words = word_tokenize(text)  # Tokenize
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    return ' '.join(words)

# Apply preprocessing
filtered_df['17_Key Findings'] = filtered_df['17_Key Findings'].astype(str).apply(preprocess_text)

# Join all the cleaned text
all_textkf = ' '.join(filtered_df['17_Key Findings'].tolist())

# Tokenize the joined text into words
all_wordskf = all_textkf.split()

# Calculate the top words
word_countskf = Counter(all_wordskf)

# Get the top 5 words
top_5_wordskf = word_countskf.most_common(5)
# Get the top 10 words
top_10_wordskf = word_countskf.most_common(10)
# Get the top 20 words
top_20_wordskf = word_countskf.most_common(20)

# Indices of the specific words you want
indiceskf = [1, 3, 5, 9, 10, 11, 12,13,14, 19]

# Extract the specific words based on the indices
selected_wordskf = [top_20_wordskf[i] for i in indiceskf]

# Print the top words
#print("Top 5 words:", top_5_wordskf)
#print("Top 10 words:", top_10_wordskf)
#print("Top 20 words:", top_20_wordskf)

# Generate the word cloud
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white', 
    max_words=100,
    max_font_size=150, 
    relative_scaling=0.5,
    normalize_plurals=False
).generate(all_textkf)

# Display the word cloud
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

# Add the top counts as a legend on the top right outside the plotting area
legend_textkf = "\n".join([f"{wordkf}: {countkf}" for wordkf, countkf in selected_wordskf])

# Draw the box around the legend
box_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")

plt.text(0.91, 0.65, legend_textkf, fontsize=7, va='top', ha='left', 
         transform=plt.gcf().transFigure, bbox=box_props)

# Text above the box
plt.text(0.91, 0.66, "Selected words \n from key \n findings", fontsize=7, va='bottom', ha='left', 
         transform=plt.gcf().transFigure, fontweight='bold')

# Save the plot
plt.savefig("/kaggle/working/Keyfind_WC_Aug6.tif", bbox_inches='tight')

# Show the plot
plt.show()
