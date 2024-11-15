######## Figure 12 panel 1: Word cloud for Outcome measure results 
############ Word_Cloud_Outcome_measure column
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Load the dataset
# /kaggle/input/406-data-aug-01/406_DataEtraction_withRiskofBias_August_01_Final.xlsx
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
    return words

# Apply preprocessing
filtered_df['16_Outcome measure results'] = filtered_df['16_Outcome measure results'].astype(str).apply(preprocess_text)

# Join all the cleaned text
all_words = [word for sublist in filtered_df['16_Outcome measure results'].tolist() for word in sublist]
all_text = ' '.join(all_words)

# Generate the word cloud
wordcloud = WordCloud(
    width=800, 
    height=400, 
    background_color='white', 
    max_words=100,
    max_font_size=150, 
    relative_scaling=0.5,
    normalize_plurals=False
).generate(all_text)

# Calculate the top 5 words
word_counts = Counter(all_words)
top_5_words = word_counts.most_common(5)
# Get the top 10 words
top_10_words = word_counts.most_common(10)
# Get the top 20 words
top_20_words = word_counts.most_common(20)
# Indices of the specific words you want
indices = [0, 3, 4, 8, 9, 10, 11, 17, 18]

# Extract the specific words based on the indices
selected_words = [top_20_words[i] for i in indices]

# Extract the 3rd to 7th words
# words_3_to_7 = top_10_words[2:7]
words_R0 = word_counts['r0']
# print(words_R0)
# Display the word cloud
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off the axis

# Add a legend with the top 5 words
#legend_text = 'Word Cloud \n of Outcome \n measure results\n\nTop 5 Words:\n'
#for word, count in top_5_words:
   # legend_text += f'{word}: {count}\n'

# Add title "Top Five" above the box
#plt.text(0.77, 0.74, "Top Five", fontsize=14, va='bottom', ha='left', 
    #     transform=plt.gcf().transFigure, fontweight='bold')


#plt.text(3, 0.741, legend_text, fontsize=12, va='top', ha='left', bbox=dict(boxstyle="round,pad=0.5", edgecolor='black', facecolor='white'))
#######################
# Add the top counts as a legend on the top right outside the plotting area
legend_text = "\n".join([f"{word}: {count}" for word, count in selected_words])
# Draw the box around the legend
box_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")

plt.text(0.78, 0.65, legend_text, fontsize=7, va='top', ha='left', 
         transform=plt.gcf().transFigure, bbox=box_props)

# Add title "Top Five" above the box
plt.text(0.77, 0.66, "Selected words \n from Outcome \n measure results", fontsize=7, va='bottom', ha='left', 
         transform=plt.gcf().transFigure, fontweight='bold')

# Ensure space for the legend
plt.subplots_adjust(right=0.75)
#############################
# Save the plot
#plt.savefig("/kaggle/working/Outcomres_Aug06.tif", bbox_inches='tight')
plt.savefig("/kaggle/working/Outcomres_Aug06_Nov03_2.tif", bbox_inches='tight')
# Show the figure
plt.show()
