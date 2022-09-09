# Gov UK dashboards

This package contains functionality which is common to UK Government plotly dashboards.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Updating](#updating)
- [Trying out changes to the package from other repositories](#Trying out changes to the package from other repositories)
- [License](#license)

## Background

This package is to enable quicker development of government data dashboards, such as the government colour schemes and plotly components.

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

For formatting:
```python
from gov_uk_dashboards.formatting.human_readable import format_as_human_readable

format_as_human_readable(1200,prefix='£')
```

For figures:
```python
from gov_uk_dashboards import figures

chart_data = figures.ChartData(
    dataframe,
    x_column = "Date",
    y_column = "Value",
    category_column = "Category"
)

line_chart = figures.line_chart(
    data = chart_data,
    title = "Chart title"
    line_style = {
        "Category 1": figures.format.LineFormat(
            color = "#000000",
            dash_pattern = figures.enums.DashPatterns.SOLID,
        ),
    }
)
```

## Updating

When making changes to the package, the following should be done:

- Update version in setup.py accordingly
    - Style: Major.Minor.Patch, e.g. 1.2.3
    - Major - any breaking changes to previous functionality.
    - Minor - additional functionality that doesn't effect backward compatibility. When updated the patch version should be reset to zero. eg. 2.3.1 goes to 2.4.0 for minor update.
    - Patch - bug fixes that don't effect backward compatibility.
    For more information see [here](https://semver.org)
- After merging with main, go [here](https://github.com/communitiesuk/pkg_gov_uk_dashboards/releases) to add a new version tag.
    - Click 'Draft a new release'
    - Under 'Choose a tag' dropdown, enter 'v&lt;version number&gt;'. Click 'Create new tag'
    - Give the tag a release title, this should be the same as the tag name.
    - Give a bullet point list of changes in the "Describe this release" section.
    - Make sure 'Target' is set to 'main'.
    - Click 'Publish release'.
- Update the package references within projects where the package is used, by following the [Installation](#Install) section.


## Trying out changes to the package from other repositories

When you want to make changes to the package to use in another repository, it can be useful to see what changes would look like before commiting to the package repo. You can do this by making changes directly to the package files in the conda environment of the repository you're working in.

- Open the file you wish to change in the conda environment
- You can do this by clicking into functions from the package in your IDE or by finding the file you wish to change in your file system, e.g.
 ```.../anaconda3/envs/local_government_dashboard/lib/python3.9/site-packages/gov_uk_dashboards/components/...```
- Make the changes to the package file and you should see the changes in your localhost on refresh

When you're happy, you can make the changes on a branch in the package repo and install it locally to check it works as expected when imported before merging into main in the package repo:
- You can update the *environment.yml* to point at your branch or run ```pip install``` with the url:
    ```git+https://github.com/communitiesuk/pkg_gov_uk_dashboards.git@<your-branch>``` 
## License

[MIT](LICENSE) Copyright (c) 2022 Crown Copyright (Department for Levelling Up, Housing and Communities)