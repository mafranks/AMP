import sys
import json
import requests
from tkinter import *

# Input your Visibility API Key information here
CLIENT_ID = ''
CLIENT_PASSWORD = ''


SESSION = requests.session()

def generate_token():
    ''' Generate a new access token and write it to disk
    '''
    url = 'https://visibility.amp.cisco.com/iroh/oauth2/token'

    headers = {'Content-Type':'application/x-www-form-urlencoded',
               'Accept':'application/json'}

    payload = {'grant_type':'client_credentials'}

    response = requests.post(url, headers=headers, auth=(CLIENT_ID, CLIENT_PASSWORD), data=payload)

    if unauthorized(response):
        sys.exit('Unable to generate new token!\nCheck your CLIENT_ID and CLIENT_PASSWORD')

    response_json = response.json()
    access_token = response_json['access_token']

    with open('threat_response_token', 'w') as token_file:
        token_file.write(access_token)

def get_token():
    ''' Get the access token from disk if it's not there generate a new one
    '''
    for i in range(2):
        while True:
            try:
                with open('threat_response_token', 'r') as token_file:
                    access_token = token_file.read()
                    return access_token
            except FileNotFoundError:
                print('threat_response_token file not found, generating new token.')
                generate_token()
            break

def inspect(observable):
    '''Inspect the provided observable and determine it's type
    '''
    inspect_url = 'https://visibility.amp.cisco.com/iroh/iroh-inspect/inspect'

    access_token = get_token()
    headers = {'Authorization':'Bearer {}'.format(access_token),
               'Content-Type':'application/json',
               'Accept':'application/json'}

    inspect_payload = {'content':observable}
    inspect_payload = json.dumps(inspect_payload)
    response = SESSION.post(inspect_url, headers=headers, data=inspect_payload)
    return response

def enrich(observable):
    ''' Query the API for a observable
    '''
    enrich_url = 'https://visibility.amp.cisco.com/iroh/iroh-enrich/deliberate/observables'

    access_token = get_token()

    headers = {'Authorization':'Bearer {}'.format(access_token),
               'Content-Type':'application/json',
               'Accept':'application/json'}

    response = SESSION.post(enrich_url, headers=headers, data=observable)

    return response

def unauthorized(response):
    ''' Check the status code of the response
    '''
    if response.status_code == 401:
        return True
    return False

def check_auth(function, param):
    ''' Query the API and validate authentication was successful
        If authentication fails, generate a new token and try again
    '''
    response = function(param)
    if unauthorized(response):
        print('Auth failed, generating new token.')
        generate_token()
        return function(param)
    return response

def query(observable):
    ''' Pass the functions and parameters to check_auth to query the API
        Return the final response
    '''
    response = check_auth(inspect, observable)
    inspect_output = response.text
    response = check_auth(enrich, inspect_output)
    return response


def main_query(_observable):
    response = query(_observable)
    response_json = response.json()
    query_output = []

    for module in response_json['data']:
        module_name = module['module']
        if 'verdicts' in module['data'] and module['data']['verdicts']['count'] > 0:
            docs = module['data']['verdicts']['docs']
            for doc in docs:
                observable_value = doc['observable']['value']
                disposition = doc.get('disposition', 'None')
                disposition_name = doc.get('disposition_name', 'None')
                query_output.append([module_name, disposition, disposition_name, observable_value])
    return query_output


def main():
    ''' Main script logic
    '''
    def click():
        _observable = e1.get()
        output.delete(0.0, END)
        results = main_query(_observable)
        if results:
            for i in results:
                output.insert(END, f"{i[0]}: {i[2]}\n")
        else:
            output.insert(END, f"No results found.")

    window = Tk()
    window.title('Disposition Query')
    window.configure(background='black')
    e1 = Entry(window, width=60, bg='black', fg='white')
    e1.grid(row=1, column=0, sticky=W)
    e1.insert(0, "Enter SHA256 hash here and click submit.")
    Button(window, text='Submit', bg='white', fg='black', width=6, command=click).grid(row=1, column=1, sticky=E)
    Label(window, text='Output:', bg='black', fg='white').grid(row=2, column=0, sticky=W)
    window.update()
    output = Text(window, width=80, height=5, wrap=WORD, background='black', fg='white')
    output.grid(row=3, column=0, columnspan=2, sticky=W)
    window.mainloop()



if __name__ == '__main__':
    main()
