import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import os

# import spacy for stopword removal and word process
import spacy

# import cunter to count cleaned words
from collections import Counter

app = dash.Dash(__name__)

data = pd.read_csv("scraped_data/metadata.csv")

# load spacy
nlp = spacy.load("en_core_web_lg")

# load and combine all transcript.txt files for a president
def load_president_text(president_name):
    base_path = "scraped_data"
    president_path = os.path.join(base_path, president_name)

    full_text = ""

    # go through all speech folders
    for speech_folder in os.listdir(president_path):
        transcript_path = os.path.join(
            president_path,
            speech_folder,
            "transcript.txt"
        )

        # read transcript if it exists
        if os.path.isfile(transcript_path):
            with open(transcript_path, encoding="utf-8") as f:
                full_text += f.read() + " "

    return full_text

# clean text by removing stopwords and non alphabetic words
def clean_text(text):
    doc = nlp(text)

    return Counter(
        word.lemma_.lower()
        for word in doc
        if word.is_alpha
        and not word.is_stop
    )

app.layout = html.Div([
    html.H1("Presidential Speeches"),
    dcc.Graph(id="bar_chart")
])

@app.callback(
    Output("bar_chart", "figure"),
    Input("bar_chart", "id")
)
def update_bar(_):
    counts = data.groupby("president_name").size().reset_index(name="count")
    fig = px.bar(counts, x="president_name", y="count")
    return fig

if __name__ == "__main__":
    app.run(debug=False, port=2525)
