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


## License

[MIT](LICENSE) Copyright (c) 2022 Crown Copyright (Department for Levelling Up, Housing and Communities)