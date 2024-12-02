import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

class VoltelloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Voltello", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("api_token"): str,
                vol.Required("customer_id"): str,
                vol.Required("utility_id"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return VoltelloOptionsFlowHandler(config_entry)

class VoltelloOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("api_token", default=self.config_entry.data.get("api_token")): str,
                vol.Required("customer_id", default=self.config_entry.data.get("customer_id")): str,
                vol.Required("utility_id", default=self.config_entry.data.get("utility_id")): str,
            })
        )