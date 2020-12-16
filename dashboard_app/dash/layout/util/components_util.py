import dash_core_components as dcc
import dash_html_components as html
import dash_table
from datetime import date


def create_import_metric_block(string_amount, class_name, child_id, child_description_text):
    """
    Created a block that shows a metric with its description.

    @param string_amount: The number shown in the block
    @param class_name: Classname of the block
    @param child_id: Id for the metric amount
    @param child_description_text: Type of metric
    @return: A div component with a metric.
    """
    div = html.Div([
                    html.Div(string_amount, id=child_id),
                    html.Div(child_description_text)
                ], className=class_name)
    return div


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


def create_datepicker(id):
    datepicker = dcc.DatePickerRange(
        id=id,
        min_date_allowed=date(2020, 1, 1),
        max_date_allowed=date(2021, 12, 31),
        start_date=date(2020, 1, 1),
        end_date=date(2020,12,31),
        display_format='D MMM YYYY'
    )
    return datepicker
