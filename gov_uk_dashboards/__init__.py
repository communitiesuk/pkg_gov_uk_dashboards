"""A package containing functionality which is common to UK Government plotly
dashboards.

Contains the following modules:
- components: Module containing submodules for building GOV.UK Design System
    dashboards using different systems.
    - plotly: Module containing Plotly/Dash components for building GOV.UK
        Design System dashboards.
- figures: Module containing standard Plotly figures for use in dashboards.
    - enums: Module containing enums used in the construction of plotly figures.
    - styles: Module containing classes & functions used for styling plotly
        figures.
- axes: Module containing functions related to graph axes.
- formatting: Module containing tools to assist with formatting of numbers in
    dashboards.
    - rounding: Module containing functions to round data to the standard
        rounding needed for display.
- colours: Module containing Enums for Gov.UK colours and ONS Accessible
    Colours.

Contains the following function:
- read_template: Return the government html template as a str for Plotly.
"""
