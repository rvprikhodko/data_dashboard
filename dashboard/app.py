import requests
import pandas as pd
from dash import Dash, dcc, html


app = Dash(__name__)
url_df = 'http://localhost:11000/files/df'

response_df = requests.get(url=url_df)
df = pd.DataFrame(response_df.json())

data = (
    df
)

app.layout = html.Div(
    children=[
        html.H1(children="Fuel Consumption Analytics"),
        html.P(
            children=(
                "Analyze the behavior of fuel consumption over the years"
                " of vehicles used between 2000 and 2022"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["YEAR"],
                        "y": data["FUEL CONSUMPTION"],
                        "type": "bar",
                    },
                ],
                "layout": {"title": "Fuel Consumption Graph"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["YEAR"],
                        "y": data["EMISSIONS"],
                        "type": "bar",
                    },
                ],
                "layout": {"title": "Emissions Graph"},
            },
        ),
    ]
)
