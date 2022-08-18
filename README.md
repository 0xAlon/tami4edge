# tami4edge for Home Assistant

This repository contains a [tami4edge](https://www.tami4.co.il/tami4edge-collection) component for [Home Assistant](https://www.home-assistant.io/).
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

![alt text](https://www.tami4.co.il/sites/default/files/2021-04/edge%2B_white_left_552x820.png)


The component is developed by [Alon Teplitsky](https://www.linkedin.com/in/alon-teplitsky/).

## Installation

Installation via [HACS](https://hacs.xyz/) (recommended) or by copying `custom_components/tami4edge` into your Home Assistant configuration directory.


## Configuration

The component requires configuration via the Home Assistant configuration file. The following parameters are required:

    tami4edge:
      api_key: API_KEY


N.B. You will need an API key from [tami4edge Cloud Token Extractor](https://github.com/0xAlon/tami4edge-Token-Extractor) to use this component.


## Entities

Each entity will be represented as a sensor with the current state of usage.

- `Daily usage`
- `Weekly Usage`
- `Average Daily Usage`
- `Water Filter`
- `UV Filter`

## buttons

The following button is implemented by the component:

- `Boil water`
