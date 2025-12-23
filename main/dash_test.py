import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import os
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# download the required nltk resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = dash.Dash(__name__)

# load the metadata
data = pd.read_csv("scraped_data/metadata.csv")

# load the "lemmatizerr" and load the english stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# load and combine all transcript.txt files for a president
def load_president_text(president_name):
    base_path = "scraped_data"
    # replace all dots etc. to match the folder naming from the parser
    safe_name = president_name.replace(" ", "_").replace(".", "")
    president_path = os.path.join(base_path, safe_name)

    full_text = ""
    if os.path.exists(president_path):
        for speech_folder in os.listdir(president_path):
            transcript_path = os.path.join(president_path, speech_folder, "transcript.txt")
            if os.path.isfile(transcript_path):
                with open(transcript_path, encoding="utf-8") as f:
                    full_text += f.read() + " "
    return full_text

# clean text by removing stopwords and non "alphabetic" words
def clean_text(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words if w.isalpha() and w.lower() not in stop_words]
    lemmatized = [lemmatizer.lemmatize(w) for w in words]
    return Counter(lemmatized)

# generate the wordcloud image
def generate_wordcloud_image(word_counts, max_words=50):
    wc = WordCloud(width=600, height=400, background_color="white",
                   max_words=max_words).generate_from_frequencies(word_counts)
    return wc.to_array()

app.layout = html.Div([
    html.H1("Presidential Speeches"),
    dcc.Graph(id="bar_chart"),
    dcc.Graph(id="wordcloud")
])

@app.callback(
    Output("bar_chart", "figure"),
    Input("bar_chart", "id")
)
def update_bar(_):
    counts = data.groupby("president_name").size().reset_index(name="count")
    fig = px.bar(counts, x="president_name", y="count")
    return fig

@app.callback(
        Output("wordcloud", "figure"),
        Input("bar_chart", "clickData")
)
def update_wordcloud(clickData):
    if not clickData:
        return go.Figure()
    
    president = clickData["points"][0]["x"]
    text = load_president_text(president)
    word_counts = clean_text(text)
    
    img = generate_wordcloud_image(word_counts)
    fig = px.imshow(img)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    return fig

if __name__ == "__main__":
    app.run(debug=False, port=2525)
