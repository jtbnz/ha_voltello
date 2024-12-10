import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

DOMAIN = "voltello"

class VoltelloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required("api_token"): str,
                    vol.Required("customer_id"): str,
                    vol.Required("utility_id"): str,
                })
            )

        return self.async_create_entry(
            title="Voltello Energy Monitor",
            data=user_input
        )