"""get_chart_for_download"""

from gov_uk_dashboards.constants import MAIN_TITLE, SUBTITLE


def get_chart_for_download(self, fig):
    """Returns a fig with title and subtitle for download as png"""
    main_title = self.title_data[MAIN_TITLE]
    subtitle = self.title_data[SUBTITLE]
    footnote = getattr(self, "footnote", None)

    fig.update_layout(
        title={
            "text": f"<b><span style='color: black; margin: 0px 0px 5px'>{main_title}</span></b>",
            "x": 0.01,
            "xanchor": "left",
        },
        title_subtitle={
            "text": f"<b><span style='color: black; margin: 0px 0px 5px'>{subtitle}</span></b>"
        },
        annotations=(
            [
                {
                    "text": f"<span style='color: black; fontSize: 18px;'>{footnote}</span>",
                    "x": -0.01,
                    "y": -0.4,  # Bottom of the plotting area
                    "xref": "paper",
                    "yref": "paper",
                    "xanchor": "left",
                    "yanchor": "top",
                    "showarrow": False,
                    "align": "left",
                }
            ]
            if footnote is not None
            else []
        ),
    )
    return fig
