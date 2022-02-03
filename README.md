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
pip install git+https://github.com/communitiesuk/Plotly_utilities.git
```

For installation using conda, paste the following code into the environment configuration file:

```yml
 - pip:
     - git+https://github.com/communitiesuk/Plotly_utilities.git
```


## Usage

In order to access the colours in the package, use the command:

```python
from gov_uk_dashboards.colours.colours import GovUKColours

GovUKColours.DLUHC_BLUE.value
```

For components:
```python
from gov_uk_dashboards.components.plotly import banners

banners.message_banner('category','message')
```


## License

[MIT](LICENSE) Copyright (c) 2022 Crown Copyright (Department for Levelling Up, Housing and Communities)