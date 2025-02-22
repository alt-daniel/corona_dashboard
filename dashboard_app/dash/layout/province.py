from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from config import Config
import util.file_util as ut
from dashboard_app.dash.data import data_metrics as dm
from dashboard_app.dash.layout.util import components_util as cu

def get_province_layout(app):

    provinces = ["Flevoland", "Noord-Holland", "Friesland", "Zuid-Holland", "Zeeland",
                 "Noord-Brabant", "Gelderland", "Overijssel", "Limburg", "Drenthe", "Groningen", "Utrecht"]

    groupby_types = {
        "Municipality_name": "Gemeente",
        "Province": "Provincie"
    }


    statistics = [["Deceased", "Overleden"], ["Hospital_admission", "Ziekenhuis Opnames"], ["Total_reported", "Aantal positief"]]

    df = ut.create_csv_from_dataframe(Config.STATIC_DATA_DIR + '/COVID-19_aantallen_gemeente_per_dag.csv')
    df2 = df.loc[df['Date_of_publication'].between('2020-01-01', '2020-12-12')].groupby(['Municipality_name', 'Province'], as_index=False).sum()

    layout = html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        cu.create_import_metric_block(str(0), "important-metric-block col",
                                                   "important-metric-municipalities", "Gemeentes", "important-metric-municipalities-description"),
                        cu.create_import_metric_block(0, "important-metric-block col",
                                                   "important-metric-deceased", "Overleden"),
                        cu.create_import_metric_block(0, "important-metric-block col",
                                                   "important-metric-hospital-admission", "Ziekenhuisopnames"),
                        cu.create_import_metric_block(0, "important-metric-block col",
                                                   "important-metric-total-reported", "Positief getest")
                    ], className="row"),
                    html.Div([
                        html.H2("Select statistic", id="histogram-statistic-title"),
                        cu.create_dropdown("statistic-selector", statistics),
                        html.H2("Group on type:", id="c-title"),
                        cu.create_radio_items(groupby_types, "groupby-radio-items"),
                        html.H2("Select a start and end date"),
                        cu.create_datepicker("statistics-datepicker"),
                        html.H2("Select a min and max value"),
                        dcc.RangeSlider(
                            id="statistic-rangeslider",
                            tooltip={'placement': 'bottom'}
                        )], id="left-overview-header-container")
                ], id="left-overview-header", className="col-4"),
                    html.Div([
                        html.Div([
                            dcc.Graph(id='bar-chart-graph')
                        ], id="bar-chart-graph-container")
                    ], id="right-overview-header col", className="col-8")
            ], id="province-header", className="row"),
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
        ], className="container")
    ], id="province-container")

    init_province_callbacks(app, df, groupby_types)

    return layout


def init_province_callbacks(app, df, groupby_types):
    @app.callback(
        Output(component_id="statistic-rangeslider", component_property='min'),
        Output(component_id="statistic-rangeslider", component_property='max'),
        Output(component_id="statistic-rangeslider", component_property='value'),
        Output(component_id="statistic-rangeslider", component_property='marks'),
        Input(component_id="statistic-selector", component_property='value'),
        Input("statistics-datepicker", 'start_date'),
        Input("statistics-datepicker", 'end_date'),
        Input("groupby-radio-items", 'value')
    )
    def update_range_slider(selector_value, start_date, end_date, radio_value):

        df2 = df.loc[df['Date_of_publication'].between(start_date, end_date)].\
            groupby([radio_value], as_index=False).sum()

        min_value = df2[selector_value].min()
        max_value = df2[selector_value].max()
        range = [min_value, max_value]
        marks = {
            str(min_value): {'label': str(min_value), 'style': {'color': '#f50'}},
            str(max_value): {'label': str(max_value), 'style': {'color': '#77b0b1'}}
        }
        return min_value, max_value, range, marks


    @app.callback(
        Output(component_id="bar-chart-graph", component_property='figure'),
        Output(component_id="important-metric-municipalities", component_property='children'),
        Output(component_id="important-metric-deceased", component_property='children'),
        Output(component_id="important-metric-hospital-admission", component_property='children'),
        Output(component_id="important-metric-total-reported", component_property='children'),
        Output(component_id="important-metric-municipalities-description", component_property='children'),
        Input(component_id="statistic-selector", component_property='value'),
        Input(component_id="statistic-rangeslider", component_property='value'),
        Input("statistics-datepicker", 'start_date'),
        Input("statistics-datepicker", 'end_date'),
        Input("groupby-radio-items", 'value')
    )
    def update_bar_chart_on_range_and_selector(selector_value, rangeslider_value, start_date, end_date, radio_value):
        df2 = df.loc[df['Date_of_publication'].between(start_date, end_date)]. \
                groupby([radio_value], as_index=False).sum()
        df3 = df2.loc[df2[selector_value].between(rangeslider_value[0], rangeslider_value[1])]

        max_deceased = dm.get_total_sum_from_column(df3, "Deceased")
        max_hospital_admission = dm.get_total_sum_from_column(df3, "Hospital_admission")
        max_total_reported = dm.get_total_sum_from_column(df3, "Total_reported")


        label_radio_item = str(groupby_types.get(radio_value))

        return cu.create_bar_chart(df3, radio_value, selector_value), df3[radio_value].nunique(),\
               max_deceased, max_hospital_admission, max_total_reported, label_radio_item


    @app.callback(
        Output(component_id="database-table", component_property='data'),
        Input(component_id="province-selector", component_property='value')
    )
    def update_data_table(value):
        df2 = df.groupby(['Municipality_name', 'Province'], as_index=False).sum()
        df2 = df2.loc[df2['Province'].isin(list(value))]
        return df2.to_dict('records')









