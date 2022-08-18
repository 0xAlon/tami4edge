"""Constants for tami4edge."""

from datetime import timedelta

# Base component constants
DOMAIN = "tami4edge"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.0.0"
PLATFORMS = ["sensor","button"]

# Volume units
VOLUME_LITERS = "L"
TIME_DAYS = "Days"
DEVICE_CLASS_DATE = "date"

# Icons
DEFAULT_ICON = "mdi:cup-water"
BUTTON_ICON = "mdi:kettle-steam-outline"

# Overall scan interval
TOKEN_SCAN_INTERVAL = timedelta(hours=3)