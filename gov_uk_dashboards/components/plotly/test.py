from gov_uk_dashboards.constants import MAIN_TITLE, SUBTITLE


def test(self, fig):
    main_title = self.title_data[MAIN_TITLE]
    subtitle = self.title_data[SUBTITLE]
    
    fig.update_layout(
        title=dict(
            text=f"<b><span style='color: black; margin: 0px 0px 5px'>{main_title}</span></b>",
            x=0.01,
            xanchor="left",
        ),
        title_subtitle=dict(
            text=f"<b><span style='color: black; margin: 0px 0px 5px'>{subtitle}</span></b>"
        ),
        margin=dict(t=100),
    )
    return fig