# tami4edge for Home Assistant

# ⚠️ This project is no longer maintained

Thank you for your interest in this project.  
It is no longer actively maintained, and no further updates, bug fixes, or support will be provided.  

You are welcome to fork the repository if you’d like to continue development.

🚧 -------------------------------------------------------------------- 🚧

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

### Disclaimer
I don't have any contact with the company and am not responsible for any loss or damage caused by this integration.
