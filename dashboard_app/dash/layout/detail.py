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
        dcc.Graph(id="province-map", figure=get_province_map(df, province_geojson))
    )

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
                        labels={"Total_reported": 'Getest',
                                'Hospital_admission': 'Opname ziekenhuis'}
                        )

    # fig = px.choropleth(geojson = dutch_town)

    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_geos(visible=False, resolution=50, scope="europe",
    countrycolor="Black",
    showsubunits=True, subunitcolor="Blue")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


    return fig
