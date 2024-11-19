from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN, CONF_API_TOKEN, CONF_CUSTOMER_ID, CONF_UTILITY_ID

class VoltelloConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate the credentials here if possible
            return self.async_create_entry(
                title="Voltello",
                data={
                    CONF_API_TOKEN: user_input[CONF_API_TOKEN],
                    CONF_CUSTOMER_ID: user_input[CONF_CUSTOMER_ID],
                    CONF_UTILITY_ID: user_input[CONF_UTILITY_ID],
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_TOKEN): str,
                vol.Required(CONF_CUSTOMER_ID): str,
                vol.Required(CONF_UTILITY_ID): str,
            }),
            errors=errors,
        )