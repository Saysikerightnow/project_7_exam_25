import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import os
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# download the required nltk resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

app = dash.Dash(__name__)

# load the metadata
data = pd.read_csv("scraped_data/metadata.csv")

# load the lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# load and combine all transcript.txt files for a president
def load_president_text(president_name):
    base_path = "scraped_data"
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

# clean text by removing stopwords, non alphabetic words, and optionally filter by pos tagging
def clean_text(text, pos_filter="ALL"):
    words = word_tokenize(text)
    words = [w.lower() for w in words if w.isalpha() and w.lower() not in stop_words]
    lemmatized = [lemmatizer.lemmatize(w) for w in words]

    if pos_filter != "ALL":
        lemmatized = [w for w, t in pos_tag(lemmatized) if t.startswith(pos_filter)]

    return Counter(lemmatized)

# generate the wordcloud image
def generate_wordcloud_image(word_counts, max_words=50):
    wc = WordCloud(width=600, height=400, background_color="white",
                   max_words=max_words).generate_from_frequencies(word_counts)
    return wc.to_array()

app.layout = html.Div([
    html.H1("Presidential Speeches"),

    dcc.Graph(id="bar_chart"),

    dcc.Store(id="selected_presidents", data=[]),
    # pos dropdown
    dcc.Dropdown(
        id="pos-filter",
        options=[
            {"label": "All words", "value": "ALL"},
            {"label": "Nouns", "value": "NN"},
            {"label": "Verbs", "value": "VB"},
            {"label": "Adjectives", "value": "JJ"}
        ],
        value="ALL"
    ),

    html.Div([
        html.Div([
            dcc.Graph(id="left_wordcloud")
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            dcc.Graph(id="right_wordcloud")
        ], style={"width": "45%", "display": "inline-block"})
    ])
])

@app.callback(
    Output("bar_chart", "figure"),
    Input("bar_chart", "id")
)
def update_bar(_):
    counts = data.groupby("president_name").size().reset_index(name="count")
    fig = px.bar(counts, x="president_name", y="count")
    fig.update_layout(clickmode="event+select")
    return fig

@app.callback(
    Output("selected_presidents", "data"),
    Input("bar_chart", "clickData"),
    State("selected_presidents", "data")
)
def store_selected(clickData, selected):
    if not clickData:
        return selected

    president = clickData["points"][0]["x"]

    if president in selected:
        return selected

    selected.append(president)
    return selected[-2:]

@app.callback(
    Output("left_wordcloud", "figure"),
    Output("right_wordcloud", "figure"),
    Input("selected_presidents", "data"),
    Input("pos-filter", "value")
)
def update_wordclouds(selected, pos_filter):
    empty_fig = px.imshow(np.zeros((400,600,3), dtype=np.uint8))
    empty_fig.update_xaxes(visible=False)
    empty_fig.update_yaxes(visible=False)

    def build_fig(president):
        text = load_president_text(president)
        counts = clean_text(text, pos_filter=pos_filter)
        img = generate_wordcloud_image(counts)
        fig = px.imshow(img)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig

    if not selected:
        return empty_fig, empty_fig

    if len(selected) == 1:
        return build_fig(selected[0]), empty_fig

    return build_fig(selected[0]), build_fig(selected[1])

if __name__ == "__main__":
    app.run(debug=False, port=2525)
