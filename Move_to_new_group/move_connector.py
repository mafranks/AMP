#!/usr/bin/env python3

import requests
import json
import time
import apiCreds

# Create an apiCreds.py file in the same directory as this script with two lines:
# client_id = "1a1a1a1a1a1a1a1a1a1a"
# api_key = "1a1a1a1a-1a1a-1a1a-1a1a-1a1a1a1a1a1a"

# If you prefer, you can hard code the API credentials here with those same two lines.

client_id = apiCreds.client_id
api_key = apiCreds.api_key
auth = (client_id, api_key)

# Get list of connector GUIDs
hostnames = []
filePath = input("\nWhat is the full path of the file containing the hostnames you would like to move?\nFile Path: ").strip()
print("\n[+] Gathering hostnames....\n")
with open(filePath, 'r') as f:
    for line in f.readlines():
        hostnames.append(line.strip())

connectors = []
for hostname in hostnames:
    url = f"https://api.amp.cisco.com/v1/computers?hostname={hostname}"
    r = requests.get(url, auth=auth)
    j = json.loads(r.content)
    for item in j["data"]:
        hostname = item.get('hostname')
        guid = item.get('connector_guid')
        connectors.append((hostname, guid))
    # Adding a delay to prevent the API from being overwhelmed with requests
    time.sleep(1)

# Get available group GUIDs
print("\n[+] Gathering groups....\n")
url = "https://api.amp.cisco.com/v1/groups"
r = requests.get(url, auth=auth)
j = json.loads(r.content)
groups = []
for item in j['data']:
    groupName = item.get('name')
    groupGUID = item.get('guid')
    groups.append((groupName, groupGUID))
for index, group in enumerate(groups):
    print(f"{index+1}: {group[0]}")
groupSelection = int(input("\nPlease enter the group number you want to move connectors into.\nGroup Number: ")) - 1

# Move connectors into the new group
print("\n[+] Moving connectors....\n")
for connector in connectors:
    APICall = requests.session()
    APICall.auth = auth
    url = f"https://api.amp.cisco.com/v1/computers/{connector[1]}"
    headers = {'Content-Type': "application/x-www-form-urlencoded", 'Accept': "application/json"}
    payload = f"group_guid={groups[groupSelection][1]}"
    r = APICall.patch(url, data=payload, headers=headers)
    if r.status_code == 202:
        print(f"Connector {connector[0]} moved to {groups[groupSelection][0]}.")
    else:
        print(f"Failed to move connector, {connector[0]} to {groups[groupSelection][0]}")
    # Adding a delay to prevent the API from being overwhelmed with requests
    time.sleep(1)
