import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

app = dash.Dash(__name__)

data = pd.read_csv("scraped_data/metadata.csv")

counts = data.groupby("president_name").size().reset_index(name="count")

bar_fig = px.bar(
    counts,
    x="president_name",
    y="count"
)

bar_fig.update_layout(
    clickmode="event+select"
)


app.layout = html.Div([
    html.H1("Presidential Speeches"),

    dcc.Graph(
        id="bar_chart",
        figure=bar_fig
    ),

    dcc.Store(id="selected_presidents", data=[]),

    html.Div([
        html.Div([
            html.H3("First selection"),
            html.Div(id="left_selection")
        ], style={"width": "45%", "display": "inline-block"}),

        html.Div([
            html.H3("Second selection"),
            html.Div(id="right_selection")
        ], style={"width": "45%", "display": "inline-block"}),
    ])
])


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


@app.callback(
    Output("left_selection", "children"),
    Output("right_selection", "children"),
    Input("selected_presidents", "data")
)
def update_selection(selected):
    if not selected:
        return "", ""

    if len(selected) == 1:
        return selected[0], ""

    return selected[0], selected[1]


if __name__ == "__main__":
    app.run(debug=False, port=2727)
