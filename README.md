# tami4edge for Home Assistant

This repository contains a [tami4edge](https://www.tami4.co.il/tami4edge-collection) component for [Home Assistant](https://www.home-assistant.io/).

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

![alt text](https://www.tami4.co.il/sites/default/files/2021-04/edge%2B_white_left_552x820.png)


The component is a fork for the one that was developed by [Alon Teplitsky](https://www.linkedin.com/in/alon-teplitsky/).

## Installation

Installation via [HACS](https://hacs.xyz/) (recommended) or by copying `custom_components/tami4edge` into your Home Assistant configuration directory.

# This version does not support HA versions below 2023.07 as it uses services that can return values. 

## Configuration

The component requires configuration via the Home Assistant configuration file. The following parameters are required:

    tami4edge:
      api_key: API_KEY


N.B. You will need an API key to use this component. 

##### Get API_KEY using docker
```
docker pull 0xalon/tami4edgecloudtokenextractor:latest
docker run -it 0xalon/tami4edgecloudtokenextractor:latest
```

## Entities

Each entity will be represented as a sensor with the current state of usage.

- `Daily Water Consumption`
- `Weekly Water Consumption`
- `Average Water Consumption`
- `Filter Upcoming Replacement`
- `UV Upcoming Replacementr`

## buttons

The following buttons is implemented by the component:

- `Boil Water`
- `Sync`

## Services

The following services are implemented by the component:
- `fetch_drinks` - enable you to get all custom drinks that are configured in the app
- `prepare_drink` - prepare one of the custom drinks

### Disclaimer
I don't have any contact with the company and am not responsible for any loss or damage caused by this integration.
