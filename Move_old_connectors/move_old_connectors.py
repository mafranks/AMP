#!/usr/bin/env python3

import requests, argparse
from datetime import datetime
from AMPConfig import APIKey, ClientID

# Add the argument parsers and help menu
ap = argparse.ArgumentParser(add_help=False)
ap.add_argument("-h", "--help", action="help", default=argparse.SUPPRESS,
                help="Shows this help menu.")
ap.add_argument("-g", "--group", required=True,
                help="Group GUID to move the connectors to.")
ap.add_argument("-t", "--time", required=True,
                help="Time (in days) since the connector was last seen.")
args = ap.parse_args()

ls = {}
now = datetime.now()
comps = [i['connector_guid'] for i in requests.get("https://api.amp.cisco.com/v1/computers", auth=(ClientID, APIKey)).json()['data']]
for i in comps:
    r = requests.get("https://api.amp.cisco.com/v1/computers/{}".format(i), auth=(ClientID, APIKey)).json()['data'].get('last_seen')
    delta = None
    if len(r) > 2:
        s = datetime.strptime(r, "%Y-%m-%dT%H:%M:%SZ")
        delta = (now-s).days
    ls[i] = (r, delta+1)
for i in ls:
    move = ""
    if ls[i][1] > int(args.time):
        data = {"group_guid": args.group}
        move = requests.patch("https://api.amp.cisco.com/v1/computers/{}".format(i), data=data, auth=(ClientID, APIKey))
        if move.status_code == 202:
            print("Connector GUID "+str(i)+" was successfully moved into "+str(args.group)+" group.")
        else:
            print("There was an issue moving connector GUID "+str(i)+" to the new group.\nError: "+move.json()['errors'][0]['details'][0])

