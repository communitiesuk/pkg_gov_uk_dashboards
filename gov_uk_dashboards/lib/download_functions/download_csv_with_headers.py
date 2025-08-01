"""download_csv_with_headers"""

import io
import polars as pl
from dash import dcc
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    get_todays_date_for_downloaded_csv,
)


def download_csv_with_headers(
    list_of_df_title_subtitle_dicts: list[dict],
    name: str,
    sensitivity_label: str,
    last_updated_date: str = None,
    additional_text: list[str] = None,
):
    """
    Prepares and returns a CSV download with one or more DataFrames, each optionally preceded by
    titles, subtitles, footnotes, and metadata headers (e.g. sensitivity label, download date).

    Parameters:
        list_of_df_title_subtitle_dicts (list[dict]):
            A list of dictionaries, each containing a Polars DataFrame ('df'), a title,
            and optionally a subtitle and footnote.
        name (str):
            The filename (without extension) for the downloaded CSV.
        sensitivity_label (str):
            A label (e.g. OFFICIAL-SENSITIVE) to prepend at the top of the file.
        last_updated_date (str, optional):
            A string to indicate when the data was last updated.
        additional_text (list[str], optional):
            Extra lines to include before the data sections (e.g. disclaimers).

    Returns:
        flask.Response: A CSV file response using Dash's `dcc.send_string`.
    """
    # pylint: disable=too-many-locals
    csv_buffer = io.StringIO()
    max_columns = _get_number_of_max_columns_from_all_dfs(
        list_of_df_title_subtitle_dicts
    )
    # Get first df and first col to use to add header data
    first_df = list_of_df_title_subtitle_dicts[0]["df"]
    first_col = first_df.columns[0]

    header_data = []

    if sensitivity_label:
        header_data.append({first_col: sensitivity_label})

    header_data.extend(
        [
            {first_col: f"Date downloaded: {get_todays_date_for_downloaded_csv()}"},
            *(
                [{first_col: f"Last updated: {last_updated_date}"}]
                if last_updated_date
                else []
            ),
            {first_col: None},
            *(
                [{first_col: text} for text in additional_text] + [{first_col: None}]
                if additional_text
                else []
            ),
            {first_col: list_of_df_title_subtitle_dicts[0]["title"]},
            *(
                [{first_col: list_of_df_title_subtitle_dicts[0]["subtitle"]}]
                if list_of_df_title_subtitle_dicts[0]["subtitle"]
                else []
            ),
            {first_col: None},
            *(
                [{first_col: list_of_df_title_subtitle_dicts[0].get("footnote")}]
                if list_of_df_title_subtitle_dicts[0].get("footnote")
                else []
            ),
        ]
    )
    _write_padded_rows_to_buffer(header_data, max_columns, csv_buffer)
    for i, data in enumerate(list_of_df_title_subtitle_dicts):
        df, title, subtitle, footnote = (
            data["df"],
            data["title"],
            data["subtitle"],
            data.get("footnote"),
        )

        if i > 0 and title:
            meta_rows = [
                {first_col: title},
                *([{first_col: subtitle}] if subtitle else []),
                {first_col: None},
                *([{first_col: footnote}] if footnote else []),
            ]
            _write_padded_rows_to_buffer(meta_rows, max_columns, csv_buffer)

        # Pad DF if needed
        if df.shape[1] < max_columns:
            column_names = list(df.columns)
            header_row = {col: col for col in column_names}
            data_rows = df.to_dicts()
            data_rows.insert(0, header_row)
            padded_rows = [pad_row(row, max_columns) for row in data_rows]
            output_df = pl.DataFrame(padded_rows)
            output_df.columns = [str(i) for i in range(max_columns)]
            output_df.write_csv(csv_buffer, include_header=False)
        else:

            df.write_csv(csv_buffer)

        if i < len(list_of_df_title_subtitle_dicts) - 1:
            blank_row = pl.DataFrame([pad_row({}, max_columns)])
            blank_row.write_csv(csv_buffer, include_header=False)

    # Return CSV for download
    csv_buffer.seek(0)
    csv_data = "\ufeff" + csv_buffer.getvalue()
    return dcc.send_string(csv_data, f"{name}.csv")


def pad_row(row: dict, max_columns: int) -> dict:
    """Pad a row with None values to match max column width."""
    padded = list(row.values()) + [None] * (max_columns - len(row))
    return {str(i): val for i, val in enumerate(padded)}


def _write_padded_rows_to_buffer(
    rows: list[dict], max_columns: int, buffer: io.StringIO
):
    """Pad and write a list of rows to the CSV buffer."""
    padded_rows = [pad_row(row, max_columns) for row in rows]
    pl.DataFrame(padded_rows).write_csv(buffer, include_header=False)


def _get_number_of_max_columns_from_all_dfs(list_of_dicts: list[dict]) -> int:
    """Get max column count across all DataFrames in list."""
    return max(len(data["df"].columns) for data in list_of_dicts)
