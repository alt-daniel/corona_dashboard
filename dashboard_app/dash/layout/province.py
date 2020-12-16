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

    max_value_range_slider = df2[statistics[0]].max()
    min_value_range_slider = df2[statistics[0]].min()

    layout = html.Div([
        html.Div([
            html.H2("Select statistic", id="histogram-statistic-title"),
            dcc.Dropdown(
                id="statistic-selector",
                options=[{'label': item.replace('_', ' '), "value": item} for item in statistics],
                value=statistics[0],
                multi=False
            ),
            html.H2("Select a min and max value"),
            dcc.RangeSlider(
                id="statistic-rangeslider",
                min=min_value_range_slider,
                max=max_value_range_slider,
                value=[min_value_range_slider, max_value_range_slider],
                marks={
                    str(min_value_range_slider): {'label': str(min_value_range_slider), 'style': {'color': '#f50'}},
                    str(max_value_range_slider): {'label': str(max_value_range_slider), 'style': {'color': '#77b0b1'}}
                }
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
        Output(component_id="statistic-rangeslider", component_property='min'),
        Output(component_id="statistic-rangeslider", component_property='max'),
        Output(component_id="statistic-rangeslider", component_property='value'),
        Output(component_id="statistic-rangeslider", component_property='marks'),
        # Output(component_id="histogram-graph", component_property='figure'),
        Input(component_id="statistic-selector", component_property='value'),
        # Input(component_id="statistic-rangeslider", component_property='value')
    )
    def update_range_slider(selector_value):

        min_value = df[selector_value].min()
        max_value = df[selector_value].max()
        range = [min_value, max_value]
        marks = {
            str(min_value): {'label': str(min_value), 'style': {'color': '#f50'}},
            str(max_value): {'label': str(max_value), 'style': {'color': '#77b0b1'}}
        }
        return min_value, max_value, range, marks


    @app.callback(
        Output(component_id="histogram-graph", component_property='figure'),
        Input(component_id="statistic-selector", component_property='value'),
        Input(component_id="statistic-rangeslider", component_property='value')
    )
    def update_histogram_on_range_and_selector(selector_value, rangeslider_value):
        df2 = df.loc[df[selector_value].between(rangeslider_value[0], rangeslider_value[1])]
        return create_histogram_figure(df2, "Municipality_name", selector_value)


    @app.callback(
        Output(component_id="database-table", component_property='data'),
        Input(component_id="province-selector", component_property='value')
    )
    def update_data_table(value):
        df2 = df.loc[df['Province'].isin(list(value))]
        return df2.to_dict('records')




