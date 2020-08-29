# home-assistant-ev-charge-control
Electric Vehicle Charge Control (switch+services) component can enable/disable charging process and retrieve charging status data.
It works over http interface of _ESL's Walli LIGHT_ charging box, resp. any electric vehicle charging station built on top of _Phoenix Contact's EV Charge Control device (EM-CP-PP-ETH)_.  

The EV Charge Control will be presented as `EV Charge Control` switch in [Home Assistant](https://home-assistant.io/).
The switch entity has its state values - `Vehicle status`, `Charging duration`, `Charging current`. 
It also exposes `set_charging_current`, `enable_charging` and `disable_charging` services.

## Requirements

The EV Charge Control needs to be connected to your local network. All you need to know is the IP address of the control device and you are good to go.

## HACS installation

Add this component using HACS by searching for `Electric Vehicle Charge Control` on the `Integrations` page.

## Manual installation

Create a directory called `ev_charge_control` in the `<config directory>/custom_components/` directory on your Home Assistant instance.
Install this component by copying all files in `/custom_components/ev_charge_control/` folder from this repo into the new `<config directory>/custom_components/ev_charge_control/` directory you just created.

This is how your custom_components directory should look like:
```bash
custom_components
├── ev_charge_control
│   ├── __init__.py
│   ├── ev_charge_control.py
│   ├── manifest.json
│   ├── services.yaml
│   └── switch.py
```

## Configuration example

To enable this switch, add the following lines to your `configuration.yaml` file:

``` YAML
switch:
  - platform: ev_charge_control
    ip_address: "192.168.1.13"
```

## EV Charge Control communication testing

To test whether the EV Charge control interface properly works, just execute the `basic_test.py` script 

## References 

[ESL's Walli LIGHT](https://esl-emobility.com/de/walli-light-elektroauto-ladestation-wallbox-ladekabel-typ-2-11kw-16a-3-phasig.html)
[Phoenix Contact EV Charge Control](https://www.phoenixcontact.com/online/portal/us/?uri=pxc-oc-itemdetail:pid=2902802)
