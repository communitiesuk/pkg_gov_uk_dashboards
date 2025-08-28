# Import required functions
from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="UTF-8")

# Call setup function
setup(
    author="Department for Levelling Up, Housing and Communities",
    description="Provides access to functionality common to creating a data dashboard.",
    name="gov_uk_dashboards",
    version="26.1.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "setuptools~=59.8",
        "dash~=3.0",
        "numpy>=2.3.2",
        "dash_bootstrap_components~=2.0.3",
        "plotly~=6.2.0",
        "flask-basicauth~=0.2.0",
    ],
    include_package_data=True,
)
