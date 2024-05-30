import logging
from datetime import timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN, CONF_IP_ADDRESS, DEFAULT_SCAN_INTERVAL
#from .graphql_client import GraphQLClientWrapper

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    ip_address = entry.data[CONF_IP_ADDRESS]
    graphql_endpoint = f"https://api.srcful.dev/"
    #client = GraphQLClientWrapper(graphql_endpoint)
    #todo: fetch data from energy-api

    async def async_fetch_data():
        try:
            async with hass.helpers.aiohttp_client.async_get_clientsession() as session:
                async with session.get(f"http://{ip_address}/api/name") as response:
                    name_data = await response.json()
                async with session.get(f"http://{ip_address}/api/uptime") as response:
                    uptime_data = await response.json()
                async with session.get(f"http://{ip_address}/api/inverter") as response:
                    inverter_data = await response.json()
                async with session.get(f"http://{ip_address}/api/version") as response:
                    version_data = await response.json()
                async with session.get(f"http://{ip_address}/api/crypto") as response:
                    crypto_data = await response.json()

            return {
                "name": name_data.get("name"),
                "uptime": uptime_data,
                "inverter": inverter_data,
                "version": version_data,
                "crypto": crypto_data
            }
        except Exception as e:
            raise UpdateFailed(f"Error fetching data: {e}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_fetch_data,
        update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    for component in PLATFORMS:
        hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, component))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
