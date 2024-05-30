import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
import aiohttp
import async_timeout

from .const import DOMAIN, CONF_IP_ADDRESS

class InverterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            ip_address = user_input[CONF_IP_ADDRESS]

            # Fetch the name from the /api/name endpoint
            try:
                async with async_timeout.timeout(10):
                    async with aiohttp.ClientSession() as session:
                        async with session.get(f"http://{ip_address}/api/name") as response:
                            if response.status == 200:
                                data = await response.json()
                                gateway_name = data.get("name", "Unknown Inverter")
                                return self.async_create_entry(title=gateway_name, data=user_input)
                            else:
                                errors["base"] = "cannot_connect"
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS): str,
            }),
            errors=errors,
            description_placeholders={
                "title": "Enter your gateway IP",
                "description": "Please enter the IP address of your gateway."
            }
        )

class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(CONF_IP_ADDRESS, default=self.config_entry.options.get(CONF_IP_ADDRESS, "")): str,
            }),
            description_placeholders={
                "title": "Enter your gateway IP",
                "description": "Please enter the IP address of your gateway."
            }
        )
