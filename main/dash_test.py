
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

data = pd.read_csv("scraped_data/metadata.csv")

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

