import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
import plotly as px
import util.file_util as ut
from config import Config


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )

    df = ut.create_csv_from_dataframe(Config.STATIC_DIR + '/COVID-19_aantallen_gemeente_per_dag.csv')
    df2 = df.groupby(['Municipality_name'], as_index=False).sum().head(10)
    print(Config.STATIC_DIR)
    print(df2.columns)
    print(df2.info)
    print(df2['Deceased'].head())

    fig = px.hist_frame(df2, x="Municipality_name", y="Deceased")

    # Create Dash Layout
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(id='histogram-graph', figure=fig),
            create_data_table(df2)
        ],
        id='dash-container'
    )

    return dash_app.server


def create_data_table(df):
    table = dash_table.DataTable(
        id='database-table',
        columns = [{"name":i, "id": i} for i in df.columns],
        data = df.to_dict('records'),
        sort_action = "native",
        sort_mode = "native",
        page_size = 50
    )
    return table
