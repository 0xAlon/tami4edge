"""Constants for tami4edge."""

from datetime import timedelta

# Base component constants
DOMAIN = "tami4edge"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "1.0.1"
PLATFORMS = ["sensor", "button"]

# Volume units
VOLUME_LITERS = "L"
TIME_DAYS = "Days"

# Icons
WATER_ICON = "mdi:cup-water"
KETTLE_ICON = "mdi:kettle-steam-outline"
CALENDAR_ICON = "mdi:calendar"
SYNC_ICON = "mdi:sync-circle"

# Overall scan interval
TOKEN_SCAN_INTERVAL = timedelta(hours=3)
WATER_QUALITY_INTERVAL = timedelta(hours=1)
WATER_CONSUMPTION_INTERVAL = timedelta(hours=8)
