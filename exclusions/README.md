This script will walk you through a series of questions to filter down your Secure Endpoint exclusion sets and print details for the ones you're interested in.  If you have more than 100 exclusion sets, you'll have to add in offsets or put in an issue and I'll get around to it eventually.


Requirements:

Python version 3.10 (for match/case)

Go through the [Authentication instructions](https://developer.cisco.com/docs/secure-endpoint/#!authentication) for SecureX to integrate Secure Endpoint and create an API Client. 

Install python requirements:

    pip install requests
  
    pip install python-dotenv
