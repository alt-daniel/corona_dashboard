from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import plotly as plt
from config import Config
import util.file_util as ut
from dashboard_app.dash.data import data_metrics as dm
from dashboard_app.dash.layout.util import components_util as cu

def get_province_layout(app):

    provinces = ["Flevoland", "Noord-Holland", "Friesland", "Zuid-Holland", "Zeeland",
                 "Noord-Brabant", "Gelderland", "Overijssel", "Limburg", "Drenthe", "Groningen", "Utrecht"]

    statistics = ["Deceased", "Hospital_admission", "Total_reported"]

    df = ut.create_csv_from_dataframe(Config.STATIC_DATA_DIR + '/COVID-19_aantallen_gemeente_per_dag.csv')
    print(df['Date_of_report'].dtype)
    # df2 = df.groupby(['Municipality_name', 'Province'], as_index=False).sum()
    df2 = df.loc[df['Date_of_publication'].between('2020-01-01', '2020-12-12')].groupby(['Municipality_name', 'Province'], as_index=False).sum()

    n_of_municipalities = str(len(df2['Municipality_name'].unique()))
    max_deceased = dm.get_total_sum_from_column(df2, "Deceased")
    max_hospital_admission = dm.get_total_sum_from_column(df2, "Hospital_admission")
    max_total_reported = dm.get_total_sum_from_column(df2, "Total_reported")

    max_value_range_slider = df2[statistics[0]].max()
    min_value_range_slider = df2[statistics[0]].min()

    layout = html.Div([
        html.Div([
            html.Div([
                cu.create_import_metric_block(str(n_of_municipalities), "important-metric-block",
                                           "important-metric-municipalities", "Gemeentes"),
                cu.create_import_metric_block(max_deceased, "important-metric-block",
                                           "important-metric-deceased", "Overleden"),
                cu.create_import_metric_block(max_hospital_admission, "important-metric-block",
                                           "important-metric-hospital-admission", "Ziekenhuisopname"),
                cu.create_import_metric_block(max_total_reported, "important-metric-block",
                                           "important-metric-total-reported", "Positief getest"),
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
                        str(max_value_range_slider): {'label': str(max_value_range_slider),
                                                      'style': {'color': '#77b0b1'}}
                    },
                    tooltip={'placement': 'bottom'},
                ),
                cu.create_datepicker("statistics-datepicker")
            ], id="left-overview-header"),
            html.Div([
                dcc.Graph(id='histogram-graph', figure=create_histogram_figure(df2, "Municipality_name", "Deceased")),
            ], id="right-overview-header"),
        ], id="province-header"),
        html.Div([
            html.H2("Select Province", id="province-title"),
            dcc.Dropdown(
                id="province-selector",
                options=[{'label': item, "value": item} for item in provinces],
                value=provinces,
                multi=True
            ),
            cu.create_data_table(df2)
        ], id="province-content")
    ], id="province-container")

    init_province_callbacks(app, df)

    return layout


def create_histogram_figure(df, x, y):
    fig = plt.hist_frame(df, x=x, y=y)

    return fig


def init_province_callbacks(app, df):
    @app.callback(
        Output(component_id="statistic-rangeslider", component_property='min'),
        Output(component_id="statistic-rangeslider", component_property='max'),
        Output(component_id="statistic-rangeslider", component_property='value'),
        Output(component_id="statistic-rangeslider", component_property='marks'),
        # Output(component_id="histogram-graph", component_property='figure'),
        Input(component_id="statistic-selector", component_property='value'),
        Input("statistics-datepicker", 'start_date'),
        Input("statistics-datepicker", 'end_date')
        # Input(component_id="statistic-rangeslider", component_property='value')
    )
    def update_range_slider(selector_value, start_date, end_date):
        print(start_date)
        print(end_date)

        df2 = df.loc[df['Date_of_publication'].between(start_date, end_date)].\
            groupby(['Municipality_name', 'Province'], as_index=False).sum()

        min_value = df2[selector_value].min()
        max_value = df2[selector_value].max()
        range = [min_value, max_value]
        marks = {
            str(min_value): {'label': str(min_value), 'style': {'color': '#f50'}},
            str(max_value): {'label': str(max_value), 'style': {'color': '#77b0b1'}}
        }
        return min_value, max_value, range, marks


    @app.callback(
        Output(component_id="histogram-graph", component_property='figure'),
        Input(component_id="statistic-selector", component_property='value'),
        Input(component_id="statistic-rangeslider", component_property='value'),
        Input("statistics-datepicker", 'start_date'),
        Input("statistics-datepicker", 'end_date')
    )
    def update_histogram_on_range_and_selector(selector_value, rangeslider_value, start_date, end_date):
        df2 = df.loc[df['Date_of_publication'].between(start_date, end_date)]. \
                groupby(['Municipality_name', 'Province'], as_index=False).sum()
        df3 = df2.loc[df2[selector_value].between(rangeslider_value[0], rangeslider_value[1])]
        return create_histogram_figure(df3, "Municipality_name", selector_value)


    @app.callback(
        Output(component_id="database-table", component_property='data'),
        Input(component_id="province-selector", component_property='value')
    )
    def update_data_table(value):
        df2 = df.groupby(['Municipality_name', 'Province'], as_index=False).sum()
        df2 = df2.loc[df2['Province'].isin(list(value))]
        return df2.to_dict('records')


    # @app.callback(
    #     Input("statistics-datepicker", 'start_date'),
    #     Input("statistics-datepicker", 'end_date')
    # )
    # def filter_on_date(start_date, end_date, df_raw):
    #     print(start_date)
    #     print(end_date)








