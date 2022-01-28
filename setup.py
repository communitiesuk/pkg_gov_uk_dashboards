# Import required functions
from setuptools import setup, find_packages

# Call setup function
setup(
    author="Department for Levelling Up, Housing and Communities",
    description="Provides Gov.UK colours in a class for convenient use, see: https://design-system.service.gov.uk/styles/colour/",
    name="GOV_UK_Colours",
    packages=['GOV_UK_Colours', 'GOV_UK_Colours.*'],
    version="0.0.1",
)