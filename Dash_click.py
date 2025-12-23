#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 13:23:47 2025

@author: suwathysuthendrarajah
"""

import os
import pandas as pd
import dash_script
from dash_script import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

# Required NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")

app = dash_script.Dash(__name__)

# Load metadata
data = pd.read_csv("scraped_data/metadata.csv")

# Stopwords
stop_words = set(stopwords.words("english"))

# Load and combine all transcripts for one president
def load_president_text(president):
    base = "scraped_data"
    safe_name = president.replace(" ", "_").replace(".", "")
    path = os.path.join(base, safe_name)

    text = ""
    if os.path.exists(path):
        for folder in os.listdir(path):
            transcript = os.path.join(path, folder, "transcript.txt")
            if os.path.isfile(transcript):
                with open(transcript, encoding="utf-8") as f:
                    text += f.read() + " "
    return text

# Clean text + POS filtering (nouns only)
def clean_text_with_pos(text):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens if w.isalpha() and w.lower() not in stop_words]
    tagged = pos_tag(tokens)
    nouns = [word for word, tag in tagged if tag.startswith("NN")]
    return Counter(nouns)

# Generate wordcloud image
def make_wordcloud(counter):
    wc = WordCloud(
        width=500,
        height=350,
        background_color="white",
        max_words=60
    ).generate_from_frequencies(counter)
    return wc.to_array()

# Bar chart (chronological order preserved from data)
counts = data.groupby("president_name").size().reset_index(name="count")
bar_fig = px.bar(counts, x="president_name", y="count")
bar_fig.update_layout(clickmode="event+select")

# Layout
app.layout = html.Div([
    html.H1("Presidential Speeches"),

    dcc.Graph(id="bar_chart", figure=bar_fig),

    dcc.Store(id="selected_presidents", data=[]),

    html.Div([
        html.Div([
            html.H3(id="left_title"),
            dcc.Graph(id="left_wordcloud")
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            html.H3(id="right_title"),
            dcc.Graph(id="right_wordcloud")
        ], style={"width": "45%", "display": "inline-block"})
    ])
])

# Store up to two clicked presidents
@app.callback(
    Output("selected_presidents", "data"),
    Input("bar_chart", "clickData"),
    State("selected_presidents", "data")
)
def store_click(clickData, selected):
    if clickData is None:
        return selected

    president = clickData["points"][0]["x"]

    if president in selected:
        return selected

    selected.append(president)
    return selected[-2:]

# Update both wordclouds
@app.callback(
    Output("left_wordcloud", "figure"),
    Output("right_wordcloud", "figure"),
    Output("left_title", "children"),
    Output("right_title", "children"),
    Input("selected_presidents", "data")
)
def update_wordclouds(selected):
    empty_fig = px.imshow([[0]])
    empty_fig.update_xaxes(visible=False)
    empty_fig.update_yaxes(visible=False)

    if not selected:
        return empty_fig, empty_fig, "", ""

    def build_fig(president):
        text = load_president_text(president)
        counts = clean_text_with_pos(text)
        img = make_wordcloud(counts)
        fig = px.imshow(img)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        return fig

    if len(selected) == 1:
        return build_fig(selected[0]), empty_fig, selected[0], ""

    return (
        build_fig(selected[0]),
        build_fig(selected[1]),
        selected[0],
        selected[1]
    )

if __name__ == "__main__":
    app.run(debug=False, port=2526)
