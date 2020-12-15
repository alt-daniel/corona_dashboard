from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import plotly as plt
from config import Config
import util.file_util as ut


def get_province_layout(app):

    provinces = ["Flevoland", "Noord-Holland", "Friesland", "Zuid-Holland", "Zeeland",
                 "Noord-Brabant", "Gelderland", "Overijssel", "Limburg", "Drenthe", "Groningen", "Utrecht"]

    statistics = ["Deceased", "Hospital_admission", "Total_reported"]

    df = ut.create_csv_from_dataframe(Config.STATIC_DIR + '/COVID-19_aantallen_gemeente_per_dag.csv')
    df2 = df.groupby(['Municipality_name', 'Province'], as_index=False).sum()
    df3 = df2.loc[df2['Province'].isin(provinces)]

    layout = html.Div([
        html.Div([
            html.H2("Select statistic", id="histogram-statistic-title"),
            dcc.Dropdown(
                id="statistic-selector",
                options=[{'label': item, "value": item} for item in statistics],
                value=statistics[0],
                multi=False
            ),
            dcc.Graph(id='histogram-graph', figure=create_histogram_figure(df2, "Municipality_name", "Deceased")),
            html.H2("Select Province", id="province-title"),
            dcc.Dropdown(
                id="province-selector",
                options=[{'label': item, "value": item} for item in provinces],
                value=provinces,
                multi=True
            ),
            create_data_table(df2)
        ], id="province-header"),
        html.Div([], id="province-content")
    ], id="province-container")

    init_province_callbacks(app, df2)

    return layout


def create_histogram_figure(df, x, y):
    fig = plt.hist_frame(df, x=x, y=y)

    return fig

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


def init_province_callbacks(app, df):
    @app.callback(
        Output(component_id="database-table", component_property='data'),
        Input(component_id="province-selector", component_property='value')
    )
    def update_data_table(value):
        df2 = df.loc[df['Province'].isin(list(value))]
        return df2.to_dict('records')

    @app.callback(
        Output(component_id="histogram-graph", component_property='figure'),
        Input(component_id="statistic-selector", component_property='value')
    )
    def update_statistic_histogram(value):
        print(value)
        return create_histogram_figure(df, "Municipality_name", value)

