from custom_components.ev_charge_control.ev_charge_control import EvChargeControl
import asyncio

evse = EvChargeControl("192.168.1.13")
asyncio.run(evse.refresh())
status = evse.status
print(f"Status: {status.status}, duration: {status.duration}, current: {status.current}, "
      f"current_options: {status.current_options}, charging_enabled: {status.charging_enabled}")
asyncio.run(evse.set_charging_current(6))
print(f"Current: {status.current}")
