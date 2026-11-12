"""get_chart_for_download"""

from pathlib import Path

from PIL import ImageFont

from gov_uk_dashboards.constants import MAIN_TITLE, SUBTITLE


def get_chart_for_download(self, fig):
    """Returns a fig with title and subtitle for download as png"""
    main_title = self.title_data[MAIN_TITLE]

    subtitle = self.title_data[SUBTITLE]

    footnote = getattr(self, "footnote", None)

    wrapped_title = wrap_title(main_title, font_size=24)

    wrapped_subtitle = wrap_title(subtitle, font_size=19)

    wrapped_footnote = (
        wrap_title(footnote, font_size=18) if footnote is not None else None
    )

    fig.update_layout(
        title={
            "text": f"<b><span style='color: black; font-size: 24px; margin: 0px 0px 5px'>{wrapped_title}</span></b>",  # pylint: disable=line-too-long
            "x": 0.01,
            "xanchor": "left",
        },
        title_subtitle={
            "text": f"<b><span style='color: black; font-size: 19px; margin: 0px 0px 5px'>{wrapped_subtitle}</span></b>"  # pylint: disable=line-too-long
        },
        annotations=(
            [
                {
                    "text": f"<span style='color: black; font-size: 18px;'>{wrapped_footnote}</span>",  # pylint: disable=line-too-long
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
            if wrapped_footnote is not None
            else []
        ),
    )
    return fig


def wrap_title(text: str, max_width: int = 1200, font_size: int = 18) -> str:
    """Wrap text based on its rendered pixel width."""
    font = get_font(font_size)
    lines = []
    current_line = ""

    for word in text.split():
        candidate = f"{current_line} {word}".strip()

        if font.getlength(candidate) <= max_width:
            current_line = candidate
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "<br>".join(lines)


def get_font(font_size: int) -> ImageFont.FreeTypeFont:
    """Return an available TrueType font for measuring text width."""
    font_paths = [
        "arial.ttf",  # Windows
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    ]

    for font_path in Path("/usr/share").rglob("*.ttf"):
        print(f"TTF FONT: {font_path}")

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, font_size)
        except OSError:
            continue

    raise RuntimeError("No suitable TrueType font available")
