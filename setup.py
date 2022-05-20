# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Department for Levelling Up, Housing and Communities",
    description="Provides access to functionality common to creating a data dashboard.",
    name="gov_uk_dashboards",
    version="4.4.3",
    packages=find_packages(),
    install_requires=[
        "setuptools~=59.8.0",
        "dash~=2.0.0",
        "numpy>=1.22.0",
        "dash_bootstrap_components~=1.1.0",
        "pandas>=1.3",
        "plotly~=5.5.0",
    ],
    package_data={"": ["gov_uk_dashboards/template.html"]},
    include_package_data=True,
)
