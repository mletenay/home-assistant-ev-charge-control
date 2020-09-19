## Electric Vehicle Charge Control Component for Home Assistant.

Electric Vehicle Charge Control (switch+services) component can enable/disable charging process and retrieve charging status data.
It works over http interface of _ESL's Walli LIGHT_ charging box, resp. any electric vehicle charging station built on top of _Phoenix Contact's EV Charge Control_ device (_EM-CP-PP-ETH_).

## Configuration

``` YAML
switch:
  - platform: phoenix_contact
    ip_address: 192.168.1.13
```

### Entities
- `switch.ev_charge_control`

### Services

- `phoenix_contact.disable_charging`
- `phoenix_contact.enable_charging`
- `phoenix_contact.set_charging_current`

### Example

![EV Charge Control Switch Attributes](https://github.com/mletenay/home-assistant-ev-charge-control/blob/master/images/attributes.png)

### Documentation

Find the full documentation [here](https://github.com/mletenay/home-assistant-ev-charge-control).
