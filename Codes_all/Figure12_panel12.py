import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PIL import Image

# Function to load dataset
def load_data(filepath):
    data = pd.read_excel(filepath)
    df = pd.DataFrame(data)
    return df

# Function to preprocess text
def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text)  # Remove punctuation
    text = text.lower()  # Lowercase
    words = word_tokenize(text)  # Tokenize
    words = [word for word in words if word not in stopwords.words('english')]  # Remove stopwords
    return words

# Function for generating Word Cloud for Outcome Measure Results
def word_cloud_outcome_measure(df):
    filtered_df = df[df['Overall'] != 3].copy()
    filtered_df['17_Outcome measure results'] = filtered_df['17_Outcome measure results'].astype(str).apply(preprocess_text)

    all_words = [word for sublist in filtered_df['17_Outcome measure results'].tolist() for word in sublist]
    all_text = ' '.join(all_words)

    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, max_font_size=150).generate(all_text)

    word_counts = Counter(all_words)
    top_20_words = word_counts.most_common(20)
    indices = [0, 3, 4, 8, 9, 10, 11, 17, 18]
    selected_words = [top_20_words[i] for i in indices]

    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    legend_text = "\n".join([f"{word}: {count}" for word, count in selected_words])
    box_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")

    plt.text(0.78, 0.65, legend_text, fontsize=7, va='top', ha='left', transform=plt.gcf().transFigure, bbox=box_props)
    plt.text(0.77, 0.66, "Selected words \n from Outcome \n measure results", fontsize=7, va='bottom', ha='left', transform=plt.gcf().transFigure, fontweight='bold')

    plt.subplots_adjust(right=0.75)
    plt.savefig("/kaggle/working/Outcomres_Aug06_Nov03_2.tif", bbox_inches='tight')
    plt.show()

# Function for generating Word Cloud for Key Findings
def word_cloud_key_findings(df):
    filtered_df = df[df['Overall'] != 3].copy()
    filtered_df['18_Key Findings'] = filtered_df['18_Key Findings'].astype(str).apply(lambda text: ' '.join(preprocess_text(text)))

    all_textkf = ' '.join(filtered_df['18_Key Findings'].tolist())
    all_wordskf = all_textkf.split()

    word_countskf = Counter(all_wordskf)
    top_20_wordskf = word_countskf.most_common(20)
    indiceskf = [1, 3, 5, 9, 10, 11, 12, 13, 14, 19]
    selected_wordskf = [top_20_wordskf[i] for i in indiceskf]

    wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100, max_font_size=150).generate(all_textkf)

    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    legend_textkf = "\n".join([f"{word}: {count}" for word, count in selected_wordskf])
    box_props = dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white")

    plt.text(0.91, 0.65, legend_textkf, fontsize=7, va='top', ha='left', transform=plt.gcf().transFigure, bbox=box_props)
    plt.text(0.91, 0.66, "Selected words \n from key \n findings", fontsize=7, va='bottom', ha='left', transform=plt.gcf().transFigure, fontweight='bold')

    plt.savefig("/kaggle/working/Keyfind_WC_Aug6.tif", bbox_inches='tight')
    plt.show()

# Function for side-by-side plot of Outcome Measure Results and Key Findings
def side_by_side_outcome_key_findings():
    outcome_image = Image.open("/kaggle/working/Outcomres_Aug06_Nov03_2.tif")
    keyfindings_image = Image.open("/kaggle/working/Keyfind_WC_Aug6.tif")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    ax1.imshow(outcome_image)
    ax1.axis('off')
    ax1.set_title("Word cloud from Outcome measure results", pad=20)

    ax2.imshow(keyfindings_image)
    ax2.axis('off')
    ax2.set_title("Word cloud from Key Findings", pad=20)

    plt.tight_layout()
    plt.savefig("/kaggle/working/Both_Outcome_Keyfind_WC_Nov03.tif", bbox_inches='tight')
    plt.show()

# Main function to run all analyses
def main():
    filepath = "/kaggle/input/nov15-406-extracted/TKG-CJA-ExtractedData_406_270.xlsx"
    df = load_data(filepath)

    # Generate word clouds
    word_cloud_outcome_measure(df)
    word_cloud_key_findings(df)

    # Generate side-by-side plot of outcome measure and key findings
    side_by_side_outcome_key_findings()

if __name__ == "__main__":
    main()
