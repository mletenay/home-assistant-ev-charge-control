"""Constants for the Goodwe component."""
from datetime import timedelta

from homeassistant.components.select import DOMAIN as SELECT_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN

DOMAIN = "phoenix_contact"

PLATFORMS = [SELECT_DOMAIN, SENSOR_DOMAIN, SWITCH_DOMAIN]

DEFAULT_NAME = "EV Charger"
SCAN_INTERVAL = timedelta(seconds=30)

KEY_COORDINATOR = "coordinator"
KEY_DEVICE_INFO = "device_info"
KEY_EVSE = "evse"
