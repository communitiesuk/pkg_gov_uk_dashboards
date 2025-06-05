"""Module containing Dash components for building GOV.UK Design System dashboards.

See: https://design-system.service.gov.uk/components/

Contains:
- message_banner: Return a changelog banner to be used to communicate to the
    user when the dashboard was last updated.
- captioned_figure: Return figure with attached captions that can be read
    by a screen reader.
- card: Return a rectangle with a grey background. Mostly used to wrap
    individual visualisations.
- card_full_width: Return a card with a grey background that fits the full
    width of its parent container using CSS flexbox.
- empty_card: Return an empty card that is hidden to help keep alignment with
    rows and columns.
- collapsible_panel: Return a component that allows the user to open and close
    a collapsible panel containing child components.
- dashboard_container: Return a HTML wrapper for a whole dashboard.
- details: Return HTML component for showing a summary expandable with more
    information beneath.
- filter_panel: Return a card with a title that allows the user to select and
    filter metrics on the dashboard.
- hidden_filter: Return an empty, invisible HTML element that stands in for a
    filter component.
- footer: Return a component for a Gov.UK standard footer.
- graph: Takes a Plotly Figure and returns a responsive Dash graph with useful
    defaults.
- heading1: Return a H1 Dash component with gov.uk styling
- heading2: Return a H1 Dash component with gov.uk styling
- heading3: Return a H1 Dash component with gov.uk styling
    - HeadingSizes: Enum of sizes that can be used to manually adjust
        text size for heading function returns.
- html_list: Return either a <ul> or <ol> component, with the children set as
    a list of <li> components matching the list_items provided.
- key_value_pair: Return an element that displays a value (such as a metric)
    labelled by a key (such as the name of the metric).
- main_content: Return wrapper for the main content of the dashboard,
    containing visualisations.
- navbar: Return a navigation bar for switching between dashboards.
    - navbar_link: Return a link for use with the navbar.
    - navbar_link_active: Return a link that appears highlighted, suggesting to
        the user that they are already viewing the linked dashboard.
- side_navbar: Return a navigation bar for switching between dashboards.
    - side_navbar_link: Return a link for use with the side_navbar.
    - side_navbar_link_active: Return a link that appears highlighted,
        suggesting to the user that they are already viewing the linked
        dashboard.
- no_data_message: Return a list of strings with a message for when
    selection does not provide data.
- paragraph: Return a formatted <p> html component with the children provided.
    - ParagraphSizes: Enum for use with paragraph to specify the text size.
- phase_banner_with_feedback: Return a phase banner with a feedback link,
    which can be specified.
- row_component: Returns a horizontal row used to contain cards.
- tooltip_title: Return a tooltip component for explaining details.
- format_visualisation_commentary: Return paragraph styling commentary.
- format_visualisation_title: Return a default formatted title for a
    visualisation.
- apply_and_reset_filters_buttons: Add apply filters and reset filters buttons, whcih are aligned to
the right
- add_filter_button: Return a 'Compare to additional authority' button which is aligned to the right
"""

from .banners import message_banner
from ..plotly.captioned_figure import captioned_figure
from .card import card, empty_card
from .card_full_width import card_full_width
from .apply_and_reset_filters_buttons import apply_and_reset_filters_buttons
from .download_button import download_button
from .collapsible_panel import collapsible_panel
from .dashboard_container import dashboard_container
from .details import details
from .filter_panel import filter_panel, hidden_filter
from .footer import footer
from .graph import graph
from .heading import heading1, heading2, heading3, HeadingSizes
from .html_list import html_list
from .key_value_pair import key_value_pair
from .main_content import main_content
from .navbar import navbar, navbar_link, navbar_link_active
from .no_data_message import no_data_message
from .paragraph import paragraph, ParagraphSizes
from .phase_banner import phase_banner_with_feedback
from .row_component import row_component
from .side_navbar import side_navbar
from .tooltip_title import tooltip_title
from .visualisation_commentary import format_visualisation_commentary
from .visualisation_title import format_visualisation_title
from .comparison_la_filter_button import add_filter_button
