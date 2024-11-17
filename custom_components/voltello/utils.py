import requests

base_url = "https://acapi.vecddevau1.village.energy/xv1"
service_points_endpoint = "/get/customer/energy/electricity/servicepoints/"
securityContext = "Voltello/CUSTOMERS/Individual/"



def get_service_points_list(customer_id):
    url = f"{base_url}{service_points_endpoint}{securityContext}{customer_id}"
    params = {
        "customerId": customer_id,
        "utilityIdentifier": UTILITY_ID
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()['message']}")
        return None

def get_live_data(service_point_id):
    url = f"{base_url}{service_points_endpoint}{servicepointID}/usage/{securityContext}{CUSTOMER_ID}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "action": "getPowerForServicePoint",
        "returnFormat": "VE"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.json()['message']}")
        return None

def get_displayed_data(live_data):
    displayed_data = {}
    flow_data = live_data['data']['flowData']
    is_displayed = flow_data['isDisplayed']
    power_data = flow_data['power']

    if is_displayed['grid']:
        displayed_data['grid'] = power_data['grid']['power']
    if is_displayed['solar']:
        displayed_data['solar'] = {
            'power': power_data['solar']['power'],
            'name': power_data['solar']['endPoints'][0]['nickName']
        }
    if is_displayed['battery']:
        displayed_data['battery'] = {
            'power': power_data['battery']['power'],
            'stateOfCharge': power_data['battery']['endPoints'][0]['stateOfCharge']
        }
    if is_displayed['home']:
        displayed_data['home'] = power_data['home']['power']
    if is_displayed['ev']:
        displayed_data['ev'] = power_data['ev']['power']

    return displayed_data