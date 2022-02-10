# Plotly utilities

This package creates options for using different colours within the [GOV.UK palette](https://design-system.service.gov.uk/styles/colour/)

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [License](#license)

## Background

This package centralises the location for GovUKColours in order that it can be used in all Government dashboards. 

## Install

For installation using pip:

```sh
pip install git+https://github.com/communitiesuk/pkg_gov_uk_dashboards.git@<version>
```

For installation using conda, paste the following code into the environment configuration file:

```yml
 - pip:
     - git+https://github.com/communitiesuk/pkg_gov_uk_dashboards.git@<version>
```

**Note:** &lt;version&gt; should be formatted 'v0.0.0'. For example:

```sh
pip install git+https://github.com/communitiesuk/pkg_gov_uk_dashboards.git@v2.0.0
```

## Usage

Using Government dashboard template with dash:
```python
import dash
from gov_uk_dashboards.template import read_template

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.index_string = read_template()
```

For colours:
```python
from gov_uk_dashboards.colours import GovUKColours

GovUKColours.DLUHC_BLUE.value
```

For components:
```python
from gov_uk_dashboards.components.plotly import banners

banners.message_banner('category','message')
```

## Updating

When making changes to the package, the following should be done:

- Update version in setup.py accordingly
    - Style: Major.Minor.Patch, e.g. 1.2.3
    - Major - any breaking changes to previous functionality.
    - Minor - additional functionality that doesn't effect backward compatibility.
    - Patch - bug fixes that don't effect backward compatibility.
- After merging with main, go [here](https://github.com/communitiesuk/pkg_gov_uk_dashboards/releases) to add a new version tag.
    - Click 'Draft a new release'
    - Under 'Choose a tag' dropdown, enter 'v&lt;version number&gt;'. Click 'Create new tag'
    - Give the tag a release title, this should be the same as the tag name.
    - Give a bullet point list of changes in the "Describe this release" section.
    - Make sure 'Target' is set to 'main'.
    - Click 'Publish release'.
- Update the package references within projects where the package is used, by following the [Installation](#Install) section.

## License

[MIT](LICENSE) Copyright (c) 2022 Crown Copyright (Department for Levelling Up, Housing and Communities)