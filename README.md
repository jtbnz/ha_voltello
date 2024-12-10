# Voltello Home Assistant Integration

![Voltello Icon](icon.png)

This is a custom UNOFFICAL integration for Home Assistant to integrate with the Voltello API.



## Installation

1. Copy the `voltello` folder to your `config/custom_components` directory
2. Restart Home Assistant
3. Go to Configuration > Integrations
4. Click the "+ ADD INTEGRATION" button
5. Search for "Voltello"
6. Enter your API Token, Customer ID, and Utility ID

## Available Sensors

- Solar Power (kW)
- Grid Power (kW)
- Battery Power (kW)
- Battery State of Charge (%)
- Home Power (kW)
- EV Power (kW)

## Configuration

The following parameters are required:

- API Token
- Customer ID (Not sure how you actually get this yet!)
- Utility ID

These can be obtained from your Voltello account.