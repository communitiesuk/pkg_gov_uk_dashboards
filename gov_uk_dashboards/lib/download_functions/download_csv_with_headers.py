"""download_csv_with_headers"""
import io
import polars as pl
from dash import dcc
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    get_todays_date_for_downloaded_csv,
)


def download_csv_with_headers(
    list_of_df_title_subtitle_dicts: list[dict[str, str]],
    name: str,
    sensitivity_label: str,
    additional_text: list[str] = None,
):  # pylint: disable=too-many-locals
    """Adds a header above multiple dataframes,
    separates them with blank rows, and downloads as CSV.

    Args:
        list_of_df_title_subtitle_dicts (list[dict[]]): List of dictionaries containing keys: "df",
        "title" and "subtitle"
        name (str): Filename for CSV.
        sensitivity_label (str): Sensitivity label. Str or None.
        additional_text (list[str]): Additional text to inlcude in headers after data downloaded.
            Str or None.
    """

    csv_buffer = io.StringIO()

    column_list = list(list_of_df_title_subtitle_dicts[0]["df"].columns)
    column_dict = {column_name: column_name for column_name in column_list}
    blank_dict = {
        f"{i}": None
        for i in range(
            _get_number_of_max_columns_from_all_dfs(list_of_df_title_subtitle_dicts)
            - len(column_list)
        )
    }  # range is missing columns in first df compared to max columns across all dfs

    subtitle = list_of_df_title_subtitle_dicts[0]["subtitle"]
    footnote = list_of_df_title_subtitle_dicts[0]["footnote"]
    header_data = [
        {column_list[0]: "Date downloaded: " + get_todays_date_for_downloaded_csv()},
        *(
            [{column_list[0]: text} for text in additional_text]
            + [{column_list[0]: None}]
            if additional_text is not None
            else []
        ),
        {column_list[0]: list_of_df_title_subtitle_dicts[0]["title"]},
        *(
            [{column_list[0]: subtitle}] if subtitle is not None else []
        ),  # Uses unpacking (*) to add the subtitle row if subtitle is not None. If subtitle is
        # None, it unpacks an empty list, effectively skipping the row.
        {column_list[0]: None},  # Blank row
        *([{column_list[0]: footnote}] if footnote is not None else []),
        {**column_dict, **blank_dict},
    ]

    if sensitivity_label:
        header_data = [{column_list[0]: sensitivity_label}] + header_data

    pl.DataFrame(header_data).write_csv(csv_buffer, include_header=False)
    for i, data in enumerate(list_of_df_title_subtitle_dicts):
        df = data["df"]
        title = data["title"]
        subtitle = data["subtitle"]
        footnote = data.get("footnote")
        if i > 0 and title is not None:
            column_dict = {column_name: column_name for column_name in list(df.columns)}
            header_data = [
                {column_list[0]: title},
                *(
                    [{column_list[0]: subtitle}] if subtitle is not None else []
                ),  # Uses unpacking (*) to add the subtitle row if subtitle is not None. If
                # subtitle is None, it unpacks an empty list, effectively skipping the row.
                {column_list[0]: None},  # Blank row
                *([{column_list[0]: footnote}] if footnote is not None else []),
            ]
            pl.DataFrame(header_data).write_csv(csv_buffer, include_header=False)
        df.write_csv(csv_buffer, include_header=i > 0)

        if i < len(list_of_df_title_subtitle_dicts) - 1:
            blank_row = pl.DataFrame({df.columns[0]: [None]})
            blank_row.write_csv(csv_buffer, include_header=False)

    csv_buffer.seek(0)
    csv_data = (
        "\ufeff" + csv_buffer.getvalue()
    )  # Adding \ufeff ensures the correct character encoding is detected for £

    return dcc.send_string(csv_data, f"{name}.csv")


def _get_number_of_max_columns_from_all_dfs(list_of_df_title_subtitle_dicts):
    max_columns = 0
    index_of_max_cols = -1

    for idx, dic in enumerate(list_of_df_title_subtitle_dicts):
        # Get the DataFrame
        df = dic["df"]

        # Get the number of columns
        num_columns = df.shape[1]

        # Update if this DataFrame has more columns
        if num_columns > max_columns:
            max_columns = num_columns
            index_of_max_cols = idx

    max_columns = len(
        list(list_of_df_title_subtitle_dicts[index_of_max_cols]["df"].columns)
    )

    return max_columns
