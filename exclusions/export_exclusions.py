# Authentication steps: https://developer.cisco.com/docs/secure-endpoint/#!authentication/4-generate-secure-endpoint-api-access-token

import json
from msilib.schema import Error
import os
import requests

from dotenv import load_dotenv

load_dotenv()

# Get SecureX token
headers = {'Accept': 'application/json'}
data = {'grant_type': 'client_credentials'}
response = requests.post('https://visibility.amp.cisco.com/iroh/oauth2/token', headers=headers, data=data, auth=(os.getenv('CLIENT_ID'), os.getenv('CLIENT_PASSWORD')))
sx_token = response.json()['access_token']

# Get Secure Endpoint token
headers = {'Authorization': f'Bearer {sx_token}'}
response = requests.post('https://api.amp.cisco.com/v3/access_tokens', headers=headers)
se_token = response.json()['access_token']

# Call Secure Endpoint API to get Organization IDs
# https://api.amp.cisco.com/v3/organizations
headers = {'Authorization': f'Bearer: {se_token}'}
data = {'size': '100'}
response = requests.get('https://api.amp.cisco.com/v3/organizations', headers=headers, data=data)
orgs = []
for org in response.json()['data']:
    orgs.append({org['name']: org['organizationIdentifier']})

# Choose the Org you'd like to work with
def org_selection(orgs):
    print("Choose the Org you'd like to use:")
    count = 1
    for org in orgs:
        print(f"{count}: {list(org.keys())[0]}")
        count += 1
    choice = input("Choice: ")
    try:
        return orgs[int(choice) - 1]
    except Error as e:
        print(e)
        print(f"Choice {choice} not valid, try again.")
        org_selection(orgs)

org_id = list(org_selection(orgs).values())[0]
# print(org_id)

# Get exclusion set name, guid, os
def get_os_specific_set(os):
    headers = {'Authorization': f'Bearer: {se_token}'}
    data = {'size': '100', 'operatingSystem': os}
    response = requests.get(f'https://api.amp.cisco.com/v3/organizations/{org_id}/exclusion_sets', headers=headers, data=data)
    return response.text

def get_exclusion_sets(org_id):

    choice = input("Do you want to filter by exclusion sets by Operating System? [Y|y|Yes|yes|N|n|No|no]  ")
    match choice:
        case 'Y'|'y'|'Yes'|'yes':
            os_choice = input("Which OS set would you like? [windows|mac|linux]  ")
            match os_choice:
                case 'windows'|'mac'|'linux':
                    exclusion_sets = get_os_specific_set(os_choice)
                    return json.loads(exclusion_sets)['data']
                case _:
                    print("Choice not in 'windows', 'mac', 'linux' try again.")
                    get_exclusion_sets(org_id)
        case 'N'|'n'|'No'|'no':
            headers = {'Authorization': f'Bearer: {se_token}'}
            data = {'size': '100'}
            response = requests.get(f'https://api.amp.cisco.com/v3/organizations/{org_id}/exclusion_sets', headers=headers, data=data)
            return json.loads(response)['data']
        case _:
            print("Choice not recognized try again.")
            get_exclusion_sets(org_id)

exclusion_sets = get_exclusion_sets(org_id)    
print(exclusion_sets)

# Select specific exclusion set and print results
def export_single_exclusion_set(set, org_id):
    headers = {'Authorization': f'Bearer: {se_token}'}
    data = {'size': '100'}
    response = requests.get(f'https://api.amp.cisco.com/v3/organizations/{org_id}/exclusion_sets/{set["guid"]}/exclusions', headers=headers, data=data)
    print(f"{set['name']}: {set['guid']}")
    for exclusion in json.loads(response.text)['data']:
        print(f"\t{exclusion}")

def export_all_exclusion_sets(exclusion_sets, org_id):
    for set in exclusion_sets:
        export_single_exclusion_set(set, org_id)

def exclusion_set_selector(exclusion_sets, org_id):
    count = 1
    for set in exclusion_sets:
        print(f"{count}: {set}")
        count += 1
    print("Choose the exclusion set you'd like to export or 'all' to export all of them:")
    choice = input("Choice: ")
    if choice == 'all':
        export_all_exclusion_sets(exclusion_sets, org_id)
    else:
        try:
            export_single_exclusion_set(exclusion_sets[int(choice) - 1], org_id)
        except Error as e:
            print(e)
            print(f"Choice {choice} not valid, try again.")
            exclusion_set_selector(exclusion_sets)

exclusion_set_selector(exclusion_sets, org_id)
