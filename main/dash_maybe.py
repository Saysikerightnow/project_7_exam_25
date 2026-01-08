import pandas as pd
import dash
from dash import html, dcc, ALL, ctx
from dash.dependencies import Input, Output, State
import os
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# download the required nltk resources
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# load the metadata
data = pd.read_csv("scraped_data/metadata.csv")

# load the lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Store original text for sentence extraction
president_texts = {}

# load and combine all transcript.txt files for a president
def load_president_text(president_name):
    if president_name in president_texts:
        return president_texts[president_name]
    
    base_path = "scraped_data"
    safe_name = president_name.replace(" ", "_").replace(".", "")
    president_path = os.path.join(base_path, safe_name)

    full_text = ""
    if os.path.exists(president_path):
        for speech_folder in os.listdir(president_path):
            transcript_path = os.path.join(president_path, speech_folder, "transcript.txt")
            if os.path.isfile(transcript_path):
                try:
                    with open(transcript_path, encoding="utf-8") as f:
                        full_text += f.read() + " "
                except:
                    pass
    
    president_texts[president_name] = full_text
    return full_text

# clean text by removing stopwords, non alphabetic words, and optionally filter by pos tagging
def clean_text(text, pos_filter="ALL"):
    if not text:
        return Counter()
    
    try:
        words = word_tokenize(text)
        words = [w.lower() for w in words if w.isalpha() and w.lower() not in stop_words]
        lemmatized = [lemmatizer.lemmatize(w) for w in words]

        if pos_filter != "ALL":
            tagged = pos_tag(lemmatized)
            lemmatized = [w for w, t in tagged if t.startswith(pos_filter)]

        return Counter(lemmatized)
    except Exception as e:
        print(f"Error in clean_text: {e}")
        return Counter()

# generate the wordcloud image
def generate_wordcloud_image(word_counts, max_words=50):
    if not word_counts or len(word_counts) == 0:
        # Return a white image with text if no words
        img = np.ones((400, 600, 3), dtype=np.uint8) * 255
        return img
    
    try:
        wc = WordCloud(
            width=600, 
            height=400, 
            background_color="white",
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(word_counts)
        return wc.to_array()
    except Exception as e:
        print(f"Error generating wordcloud: {e}")
        # Return a white image on error
        img = np.ones((400, 600, 3), dtype=np.uint8) * 255
        return img

# Find sentences containing a specific word
def find_sentences_with_word(text, word):
    if not text:
        return []
    
    try:
        sentences = sent_tokenize(text)
        word_lower = word.lower()
        matching_sentences = []
        
        for sentence in sentences:
            words = word_tokenize(sentence)
            lemmatized = [lemmatizer.lemmatize(w.lower()) for w in words if w.isalpha()]
            
            if word_lower in lemmatized:
                matching_sentences.append(sentence)
        
        return matching_sentences
    except Exception as e:
        print(f"Error finding sentences: {e}")
        return []

# Create clickable word buttons
def create_word_buttons(word_counts, side, max_words=30):
    if not word_counts or len(word_counts) == 0:
        return html.Div("No words available", style={'textAlign': 'center', 'color': '#999'})
    
    top_words = word_counts.most_common(max_words)
    if not top_words:
        return html.Div("No words available", style={'textAlign': 'center', 'color': '#999'})
    
    buttons = []
    for word, count in top_words:
        buttons.append(
            html.Button(
                f"{word} ({count})",
                id={'type': f'{side}-word-btn', 'word': word},
                style={
                    'margin': '3px',
                    'padding': '6px 12px',
                    'backgroundColor': '#007bff' if side == 'left' else '#28a745',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                    'fontSize': '13px'
                },
                n_clicks=0
            )
        )
    
    return html.Div([
        html.P("Click a word to see sentences containing it:", 
               style={'fontWeight': 'bold', 'marginBottom': '10px', 'textAlign': 'center'}),
        html.Div(buttons, style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'})
    ])

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
            dcc.Graph(id="left_wordcloud"),
            html.Div(id="left_word_buttons", style={'margin': '10px'}),
            html.Div(id="left_sentences", style={
                'maxHeight': '300px',
                'overflowY': 'auto',
                'padding': '10px',
                'border': '1px solid #ddd',
                'margin': '10px'
            })
        ], style={"width": "45%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            dcc.Graph(id="right_wordcloud"),
            html.Div(id="right_word_buttons", style={'margin': '10px'}),
            html.Div(id="right_sentences", style={
                'maxHeight': '300px',
                'overflowY': 'auto',
                'padding': '10px',
                'border': '1px solid #ddd',
                'margin': '10px'
            })
        ], style={"width": "45%", "display": "inline-block", "verticalAlign": "top"})
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
    Output("left_word_buttons", "children"),
    Input("selected_presidents", "data"),
    Input("pos-filter", "value")
)
def update_left_wordcloud(selected, pos_filter):
    empty_img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    empty_fig = px.imshow(empty_img)
    empty_fig.update_xaxes(visible=False)
    empty_fig.update_yaxes(visible=False)
    empty_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    
    if not selected or len(selected) == 0:
        return empty_fig, html.Div()
    
    try:
        president = selected[0]
        text = load_president_text(president)
        
        if not text:
            return empty_fig, html.Div("No text available", style={'textAlign': 'center', 'color': '#999'})
        
        counts = clean_text(text, pos_filter=pos_filter)
        
        if not counts or len(counts) == 0:
            return empty_fig, html.Div("No words found", style={'textAlign': 'center', 'color': '#999'})
        
        img = generate_wordcloud_image(counts, max_words=50)
        fig = px.imshow(img)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        
        buttons = create_word_buttons(counts, 'left', max_words=30)
        
        return fig, buttons
    except Exception as e:
        print(f"Error in update_left_wordcloud: {e}")
        return empty_fig, html.Div(f"Error: {str(e)}", style={'textAlign': 'center', 'color': 'red'})

@app.callback(
    Output("right_wordcloud", "figure"),
    Output("right_word_buttons", "children"),
    Input("selected_presidents", "data"),
    Input("pos-filter", "value")
)
def update_right_wordcloud(selected, pos_filter):
    empty_img = np.ones((400, 600, 3), dtype=np.uint8) * 255
    empty_fig = px.imshow(empty_img)
    empty_fig.update_xaxes(visible=False)
    empty_fig.update_yaxes(visible=False)
    empty_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    
    if not selected or len(selected) < 2:
        return empty_fig, html.Div()
    
    try:
        president = selected[1]
        text = load_president_text(president)
        
        if not text:
            return empty_fig, html.Div("No text available", style={'textAlign': 'center', 'color': '#999'})
        
        counts = clean_text(text, pos_filter=pos_filter)
        
        if not counts or len(counts) == 0:
            return empty_fig, html.Div("No words found", style={'textAlign': 'center', 'color': '#999'})
        
        img = generate_wordcloud_image(counts, max_words=50)
        fig = px.imshow(img)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        
        buttons = create_word_buttons(counts, 'right', max_words=30)
        
        return fig, buttons
    except Exception as e:
        print(f"Error in update_right_wordcloud: {e}")
        return empty_fig, html.Div(f"Error: {str(e)}", style={'textAlign': 'center', 'color': 'red'})

@app.callback(
    Output("left_sentences", "children"),
    Input({'type': 'left-word-btn', 'word': ALL}, 'n_clicks'),
    State("selected_presidents", "data"),
    State({'type': 'left-word-btn', 'word': ALL}, 'id'),
    prevent_initial_call=True
)
def update_left_sentences(n_clicks_list, selected, button_ids):
    if not selected or not button_ids:
        return html.P("Click a word to see sentences")
    
    triggered_id = ctx.triggered_id
    if not triggered_id or not isinstance(triggered_id, dict):
        return html.P("Click a word to see sentences")
    
    word = triggered_id.get('word')
    if not word:
        return html.P("Click a word to see sentences")
    
    text = load_president_text(selected[0])
    sentences = find_sentences_with_word(text, word)
    
    if not sentences:
        return html.Div([
            html.H4(f"No sentences found with '{word}'")
        ])
    
    return html.Div([
        html.H4(f"Sentences with '{word}' ({len(sentences)} found):"),
        html.Div([
            html.P([html.Strong(f"[{i+1}] "), sentence], 
                   style={'marginBottom': '10px'})
            for i, sentence in enumerate(sentences[:10])
        ])
    ])

@app.callback(
    Output("right_sentences", "children"),
    Input({'type': 'right-word-btn', 'word': ALL}, 'n_clicks'),
    State("selected_presidents", "data"),
    State({'type': 'right-word-btn', 'word': ALL}, 'id'),
    prevent_initial_call=True
)
def update_right_sentences(n_clicks_list, selected, button_ids):
    if len(selected) < 2 or not button_ids:
        return html.P("Click a word to see sentences")
    
    triggered_id = ctx.triggered_id
    if not triggered_id or not isinstance(triggered_id, dict):
        return html.P("Click a word to see sentences")
    
    word = triggered_id.get('word')
    if not word:
        return html.P("Click a word to see sentences")
    
    text = load_president_text(selected[1])
    sentences = find_sentences_with_word(text, word)
    
    if not sentences:
        return html.Div([
            html.H4(f"No sentences found with '{word}'")
        ])
    
    return html.Div([
        html.H4(f"Sentences with '{word}' ({len(sentences)} found):"),
        html.Div([
            html.P([html.Strong(f"[{i+1}] "), sentence], 
                   style={'marginBottom': '10px'})
            for i, sentence in enumerate(sentences[:10])
        ])
    ])

if __name__ == "__main__":
    app.run(debug=True, port=2526)