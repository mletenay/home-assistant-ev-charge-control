"""Constants for the Goodwe component."""
from homeassistant.components.select import DOMAIN as SELECT_DOMAIN
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN

DOMAIN = "phoenix_contact"

PLATFORMS = [SELECT_DOMAIN, SENSOR_DOMAIN]

DEFAULT_NAME = "EV Charger"
