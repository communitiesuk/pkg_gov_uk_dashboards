"""html list component"""

from dash import html


def html_list(
    list_items: list[str], *, numbered_list: bool = False, extra_spacing: bool = False
):
    """Create either a <ul> or <ol> component, with the children set as a list of <li>
    components matching the list_items provided.
    """
    li_items = [html.Li(x) for x in list_items]

    classes = ["govuk-list"]
    if extra_spacing:
        classes.append("govuk-list--spaced")

    if numbered_list:
        classes.append("govuk-list--number")
        return html.Ol(li_items, className=" ".join(classes))

    classes.append("govuk-list--bullet")
    return html.Ul(li_items, className=" ".join(classes))
