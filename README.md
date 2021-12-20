[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

# home-assistant-ev-charge-control

Electric Vehicle Charge Control (switch+services) component can enable/disable charging process and retrieve charging status data.
It works over http interface of _ESL's Walli LIGHT_ charging box, resp. any electric vehicle charging station built on top of _Phoenix Contact's EV Charge Control_ device (_EM-CP-PP-ETH_).

The EV Charge Control will be presented as `EV Charge Control` switch in [Home Assistant](https://home-assistant.io/).  
The `switch.ev_charge_control` entity has its state values - `Vehicle status`, `Charging duration`, `Charging current`.  
It also exposes `phoenix_contact.set_charging_current`, `phoenix_contact.enable_charging` and `phoenix_contact.disable_charging` services.

## Requirements

The EV Charge Control needs to be connected to your local network.
To enable remote charging enable/disable, the DIP switch 10 has to be turned ON.

## HACS installation

Add this component using HACS by searching for `Electric Vehicle Charge Control` on the `Integrations` page.

## Manual installation

Create a directory called `phoenix_contact` in the `<config directory>/custom_components/` directory on your Home Assistant instance.
Install this component by copying all files in `/custom_components/phoenix_contact/` folder from this repo into the new `<config directory>/custom_components/phoenix_contact/` directory you just created.

This is how your custom_components directory should look like:

```bash
custom_components
├── phoenix_contact
│   ├── __init__.py
│   ├── ev_charge_control.py
│   ├── manifest.json
│   ├── services.yaml
│   └── switch.py
```

## EV Charge Control communication testing

To test whether the EV Charge control interface properly works, just execute the `basic_test.py` script

## References

[ESL's Walli LIGHT](https://esl-emobility.com/de/walli-light-elektroauto-ladestation-wallbox-ladekabel-typ-2-11kw-16a-3-phasig.html)  
[Phoenix Contact EV Charge Control](https://www.phoenixcontact.com/online/portal/us/?uri=pxc-oc-itemdetail:pid=2902802)
