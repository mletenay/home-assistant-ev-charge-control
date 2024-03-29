"""Constants for the Goodwe component."""
from datetime import timedelta

from homeassistant.const import Platform

DOMAIN = "phoenix_contact"

PLATFORMS = [Platform.SWITCH, Platform.SELECT, Platform.SENSOR]

DEFAULT_NAME = "Electric Vehicle Charger"
SCAN_INTERVAL = timedelta(seconds=30)

KEY_COORDINATOR = "coordinator"
KEY_DEVICE_INFO = "device_info"
KEY_EVSE = "evse"
