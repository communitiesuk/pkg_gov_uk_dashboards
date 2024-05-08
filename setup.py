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
    version="9.38.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "setuptools~=59.8",
        "dash~=2.0",
        "numpy>=1.22.0",
        "dash_bootstrap_components~=1.1",
        "pandas>=1.3",
        "plotly~=5.5",
        "flask-basicauth~=0.2.0",
    ],
    include_package_data=True,
)
