"""Simple test script to check EV Charge Control communication"""
from custom_components.phoenix_contact.ev_charge_control import EvChargeControl
import asyncio
import simplejson as json

evse = EvChargeControl("192.168.1.13")
asyncio.run(evse.refresh())
print(json.dumps(evse.status, default=lambda o: o.__dict__, sort_keys=False, indent=4))
asyncio.run(evse.set_charging_current(6))
print(f"Current: {evse.status.current}")
