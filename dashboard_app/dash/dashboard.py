import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
import dash_table
from dash.dependencies import Input, Output
import plotly as px
import util.file_util as ut
from .layout import province, detail
from config import Config


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            dbc.themes.BOOTSTRAP,
           'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css'
        ]
    )

    # Create Dash Layout
    # dash_app.layout = html.Div([
    #     dcc.Location(id='url', refresh=False),
    #     dcc.Tabs(
    #         id="nav-tabs", value="tab-1", children=[
    #             dcc.Tab(label="Municipality", value="tab-1"),
    #             dcc.Tab(label="Province", value="tab-2")
    #         ]
    #     ),
    #     html.Div(id="dash-container")
    # ])

    dash_app.layout = html.Div([
        dcc.Tabs([
                dcc.Tab(label="Overview", children=[province.get_province_layout(dash_app)]),
                dcc.Tab(label="Detail", children=[detail.get_detail_layout(dash_app)])
        ])
    ])

    ## TODO: Find out why these callbacks conflict with callbacks from external file on page refresh (CMD+R)
    # init_tab_callbacks(dash_app)

    return dash_app.server

# def init_tab_callbacks(app):
#     @app.callback(Output('dash-container', 'children'), Input('nav-tabs', 'value'))
#     def render_tab_content(tab):
#         if tab == 'tab-1':
#             return province.get_province_layout(app)
#         elif tab == 'tab-2':
#             return html.Div([
#                         html.H3('Content tab2')
#             ])









