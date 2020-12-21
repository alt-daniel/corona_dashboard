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
import json
from urllib.request import urlopen

def get_detail_layout(dashboard_app):
    df = ut.create_csv_from_dataframe(Config.STATIC_DATA_DIR + '/COVID-19_aantallen_gemeente_per_dag.csv')
    province_geojson = Config.STATIC_DATA_DIR + "/the-netherlands.geojson"


    layout = html.Div(
        html.Div(id="detail-container", children=[
            html.Div(id="detail-header"),
            html.Div(id="detail-content", children=[
                html.Div(className="row", children=[
                    html.Div(className="col-6", children=[
                        dcc.Graph(id="province-map", figure=get_province_map(df, province_geojson))
                    ]),
                    html.Div(className="col-6")
                ])
            ])

        ]),
    )

    init_detail_callbacks(dashboard_app)

    return layout


def get_province_map(df, geojson):
    with open(geojson) as response:
        dutch_town = json.load(response)

    df2 = df.groupby(['Province'], as_index=False).sum()


    fig = px.choropleth(df2, geojson=dutch_town,
                        locations='Province', color="Total_reported",
                        featureidkey='properties.name',
                        color_continuous_scale="Viridis",
                        range_color=(df2["Total_reported"].min(), df2["Total_reported"].max()),
                        hover_data=['Hospital_admission', 'Deceased'],
                        labels={"Total_reported": 'Getest',
                                "Deceased: Overleden"
                                'Hospital_admission': 'Opname ziekenhuis'},
                        )

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_geos(visible=False, resolution=110, scope="europe",
    countrycolor="Black",
    showsubunits=True, subunitcolor="Blue")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(marker_line_color="#FFFFFF")


    return fig


def init_detail_callbacks(app):

    @app.callback(
        Input("province-map", "clickData")
    )
    def update_choropleth_on_hover(province):
        # province.update_traces(marker_line_color="#FFFFFF")
        #
        # return province
        print(province)


