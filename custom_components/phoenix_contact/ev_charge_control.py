"""Package for reading data and managing EV Charge Control (e.g. EM-CP-PP-ETH device by Phoenix Contact)"""
import aiohttp
import logging
from aiohttp import ServerDisconnectedError
from html.parser import HTMLParser

_LOGGER = logging.getLogger(__name__)

STATUS_MAP = {
    "A": "No vehicle",
    "B": "Connected",
    "C": "Charging",
    "D": "Charging w/ ventilation",
    "E": "Error E",
    "F": "Error F",
}


class EvChargeControlStatus:
    """Electric Vehicle Charge Control status class"""

    def __init__(self):
        self.serial = None
        self.status = None
        self.current = None
        self.current_options = []
        self.duration = None
        self.charging_enabled = False


class _StatusPageParser(HTMLParser):
    def __init__(self, evse):
        super().__init__()
        self._evse = evse
        self._select_name = None

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            atrrs = dict(attrs)
            if atrrs.get("name") == "status":
                self._evse.status = atrrs.get("value")
            elif atrrs.get("name") == "loadActive":
                self._evse.duration = atrrs.get("value")
        elif tag == "select":
            atrrs = dict(attrs)
            if atrrs.get("name") == "current":
                self._select_name = "current"
                self._evse.current_options = []
            else:
                self._select_name = None
        elif tag == "option" and self._select_name:
            atrrs = dict(attrs)
            if self._select_name == "current":
                self._evse.current_options.append(atrrs.get("value"))
                if "selected" in atrrs:
                    self._evse.current = atrrs.get("value")

    def error(self, message):
        pass


class _ConfigPageParser(HTMLParser):
    def __init__(self, evse):
        super().__init__()
        self._evse = evse
        self._select_name = None

    def handle_starttag(self, tag, attrs):
        if tag == "select":
            atrrs = dict(attrs)
            if atrrs.get("name") == "remoteCharging":
                self._select_name = "remoteCharging"
            else:
                self._select_name = None
        elif tag == "option" and self._select_name:
            atrrs = dict(attrs)
            if self._select_name == "remoteCharging":
                if "selected" in atrrs:
                    self._evse.charging_enabled = atrrs.get("value") == "1"

    def error(self, message):
        pass


class _NetworkPageParser(HTMLParser):
    def __init__(self, evse):
        super().__init__()
        self._evse = evse
        self._select_name = None

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            atrrs = dict(attrs)
            if atrrs.get("name") == "serial":
                self._evse.serial = atrrs.get("value")

    def error(self, message):
        pass


class EvChargeControl(object):
    """Electric Vehicle Charge Control management class"""

    def __init__(self, ip_address):
        self._url_root = "http://" + ip_address
        self.status = EvChargeControlStatus()

    async def _get(self, url):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    self._url_root + url, allow_redirects=False
                ) as response:
                    return await response.text()
            except ServerDisconnectedError as ex:
                if ex.message.code != 303:
                    raise ex

    async def refresh(self):
        """Get the latest data from the source and updates the state."""
        data = await self._get("/network.html")
        parser = _NetworkPageParser(self.status)
        parser.feed(data)
        parser.close()
        data = await self._get("/charge.html")
        parser = _StatusPageParser(self.status)
        parser.feed(data)
        parser.close()
        data = await self._get("/config.html")
        parser = _ConfigPageParser(self.status)
        parser.feed(data)
        parser.close()

    async def set_charging_enabled(self, value):
        """Enable or disable the charging"""
        if value:
            await self._get("/config.html?remoteCharging=1")
        else:
            await self._get("/config.html?remoteCharging=0")
        await self.refresh()
        return self.status.charging_enabled

    async def set_charging_current(self, value):
        """Set the charging current"""
        # ensure string and strip optional suffix
        value = str(value).strip(" A")
        if value in self.status.current_options:
            await self._get("/charge.html?current=" + value)
        else:
            _LOGGER.debug("Invalid current value %s", value)
        await self.refresh()
        return self.status.current

    def get_vehicle_status(self):
        """Answer verbose status of the vehicle charging process"""
        return STATUS_MAP.get(self.status.status, "???")
