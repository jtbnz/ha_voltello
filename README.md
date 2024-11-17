# Voltello Home Assistant Integration

This is a custom integration for Home Assistant to integrate with the Voltello API.

## Installation

1. Clone this repository into your Home Assistant `custom_components` directory:
    ```sh
    git clone https://github.com/yourusername/ha_voltello.git custom_components/voltello
    ```

2. Restart Home Assistant.

3. Go to Configuration -> Integrations and click the "+" button to add a new integration.

4. Search for "Voltello" and follow the setup instructions.

## Configuration

You will need to provide the following information during setup:
- API Token
- Customer ID
- Utility ID

## HACS Installation TO BE DONE

To add this integration to HACS in the future:
1. Go to HACS -> Integrations -> "+" button.
2. Add this repository URL: `https://github.com/jtbnz/ha_voltello` as a custom repository.
3. Follow the installation instructions.

## Usage

Once configured, the integration will create sensors for solar, grid, battery, home, and EV power data. These sensors can be used in the Home Assistant energy dashboard and other automations.