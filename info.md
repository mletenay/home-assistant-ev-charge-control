## Electric Vehicle Charge Control Component for Home Assistant.

Electric Vehicle Charge Control (switch+services) component can enable/disable charging process and retrieve charging status data.
It works over http interface of ESL's Walli LIGHT charging box, resp. any electric vehicle charging station built on top of Phoenix Contact's EV Charge Control device (EM-CP-PP-ETH).  

## Configuration

``` YAML
switch:
  - platform: ev_charge_control
    ip_address: "192.168.1.13"
```

### Documentation

Component creates an `EV Charge Control` switch entity and exposes `set_charging_current`, `enable_charging` and `disable_charging` services.
The switch entity also exposes its state values - `Vehicle status`, `Charging duration`, `Charging current`. 

Find the full documentation [here](https://github.com/mletenay/home-assistant-ev-charge-control).