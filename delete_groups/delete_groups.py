import requests
import json

client_id = ""
api_key = ""
auth = (client_id, api_key)
group_pairs = {}
filePath = input("\nWhat is the full path of the file containing the group names you would like to delete?\nFile Path: ").strip()

def delete_groups():
    
    with open(filePath, 'r') as f:
        for line in f.readlines():
            try:
                print(f"[+] Deleting group ({line.strip()}, {group_pairs.get(line.strip())})")
                url = f"https://api.amp.cisco.com/v1/groups/{group_pairs.get(line.strip())}"
                status = requests.delete(url, auth=auth)
                if status.status_code == 200:
                    print(f"[+] {line.strip()} successfully deleted")
                else:
                    print(f"[-] Error encountered deleting {line.strip()}.  Deletion request status code: {status.status_code}")
            except:
                print(f"Unable to delete group {line.strip()} due to unknown error")

def get_group_guids():
    print("\n[+] Gathering group guids from group names.\n")
    url = "https://api.amp.cisco.com/v1/groups"
    r = requests.get(url, auth=auth)
    groups = json.loads(r.content)
    for x in groups['data']:
        group_pairs[x['name']] = x['guid']
    delete_groups()

get_group_guids()
