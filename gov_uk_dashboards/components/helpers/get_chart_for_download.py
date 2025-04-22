"""get_chart_for_download"""
from gov_uk_dashboards.constants import MAIN_TITLE, SUBTITLE


def get_chart_for_download(self, fig):
    """Returns a fig with title and subtitle for download as png"""
    main_title = self.title_data[MAIN_TITLE]
    subtitle = self.title_data[SUBTITLE]

    fig.update_layout(
        title={
            "text": f"<b><span style='color: black; margin: 0px 0px 5px'>{main_title}</span></b>",
            "x": 0.01,
            "xanchor": "left",
        },
        title_subtitle={
            "text": f"<b><span style='color: black; margin: 0px 0px 5px'>{subtitle}</span></b>"
        },
        margin={"t": 100},
    )
    return fig
