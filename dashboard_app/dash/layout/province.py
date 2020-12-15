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

    df = ut.create_csv_from_dataframe(Config.STATIC_DIR + '/COVID-19_aantallen_gemeente_per_dag.csv')
    df2 = df.groupby(['Municipality_name', 'Province'], as_index=False).sum()

    print(Config.STATIC_DIR)
    print(df.columns)
    print(df2.columns)
    print(df2.dtypes)
    print(df2['Deceased'].head())

    df3 = df2.loc[df2['Province'].isin(provinces)]
    print(df3.head(10))

    fig = plt.hist_frame(df2, x="Municipality_name", y="Deceased")

    layout = html.Div([
        html.Div([
            dcc.Graph(id='histogram-graph', figure=fig),
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

