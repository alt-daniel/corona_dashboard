from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objects as go
import plotly.express as px


def get_province_layout(app, provinces):
    layout = html.Div([
        html.Div([
            html.H2("Select Province", id="province-title"),
            dcc.Dropdown(
                id="province-selector",
                options=[{'label': item, "value": item} for item in provinces],
                value=provinces,
                multi=True
            )
        ], id="province-header"),
        html.Div([], id="province-content")
    ], id="province-container")

    return layout
