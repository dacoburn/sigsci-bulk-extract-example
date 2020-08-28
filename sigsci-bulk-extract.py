import requests, os, calendar, json, codecs
from datetime import datetime, timedelta

# Initial setup
# Base URL for the Signal Sciences Dashboard/API
api_host = 'https://dashboard.signalsciences.net/api/v0'
# e-mail address of the User with API Access for SigSci
email = os.environ.get('SIGSCI_EMAIL') or "user@email.com"
# Associated API Token of the user with API Access for SigSci
api_token = os.environ.get('SIGSCI_API_TOKEN') or "REPLACE_ME"
# API Name of the SigSci Corp
corp_name = os.environ.get('SIGSCI_CORP') or "REPLACE_ME"
# API Name of the SigSci Site/Workspace
site_name = os.environ.get('SIGSCI_SITE') or "REPLACE_ME"
# Period of time in Minutes to pull data
delta_in_minutes = os.environ.get('SIGSCI_DELTA_IN_MINUTES') or 10
# Whether to print single line JSON or multiline "pretty" JSON
pretty = os.environ.get('SIGSCI_PRETTY') or "false"
# Whether to pring one JSON per line per request or all in one Object
single_object = os.environ.get('SIGSCI_SINGLE_OBJECT') or "false"
# log_file for the script
log_file = os.environ.get('SIGSCI_LOG_FILE') or "sigsci_results.json"

# Verify the required settings are configured
if email is None or email == "" or email == "user@email.com":
    print("email option is required")
    exit(1)

if api_token is None or api_token == "" or api_token == "REPLACE_ME":
    print("api_token is required")
    exit(1)

if corp_name is None or corp_name == ""or corp_name == "REPLACE_ME":
    print("corp_name is required")
    exit(1)

if site_name is None or site_name == "" or site_name == "REPLACE_ME":
    print("site_name is required")
    exit(1)

if delta_in_minutes is None or delta_in_minutes == "" or \
        type(delta_in_minutes) != int:
    delta_in_minutes = 10

# Using lower here means we only have to do one check of the string against the
# value instead of looking for variants like True or TRUE
if pretty is not None and pretty != "" and pretty.lower() == "true":
    pretty = True
else:
    pretty = False

if single_object is not None and single_object != "" and \
        single_object.lower() == "true":
    single_object = True
else:
    single_object = False

try:
    os.remove(log_file)
except OSError as e:
    pass


# General Functions

# Definition for writing out to a log file. If the log file is not specified
# then it will print to STDOUT instead.
def logOut(msg):
    if log_file is None or log_file == "":
        print(msg)
    else:
        log = codecs.open(log_file, "a", "utf-8-sig")
        data = "%s" % (msg)
        log.write(data)
        log.write("\n")
        log.close

# Very simple function for pretty printing the JSON
def prettyJson(data):
    return(json.dumps(data, indent=4, separators=(',', ': ')))

# Calculate UTC timestamps for the time period specified in the delta
# The timestamp needs to be a Unix Epoch Timestamp
until_time = datetime.utcnow() - timedelta(minutes=5)
until_time = until_time.replace(second=0, microsecond=0)
from_time = until_time - timedelta(minutes=int(delta_in_minutes))
until_time = calendar.timegm(until_time.utctimetuple())
from_time = calendar.timegm(from_time.utctimetuple())


# Create the headers needed to authenticate
headers = {
    'Content-type': 'application/json',
    'x-api-user': email,
    'x-api-token': api_token
}
# build the API URL for the Bulk Extract API
url = api_host + ('/corps/%s/sites/%s/feed/requests?from=%s&until=%s' % (corp_name, site_name, from_time, until_time))

# Used to break out of the loop once all of the results are pulled
first = True

# Simple counter for displaying how many pages of results have been pulled
counter = 1

# Variable with a list to append each individual request to.
all_requests = []

# Loop for calling the Bulk Extract API. This will loop through until there is 
# no "next" URL to call.
while True:
    # Print out what page of results is being pulled
    page_msg = "Results Page %s" % counter
    print(page_msg)

    # Actual call to the requests library to pull results
    response_raw = requests.get(url, headers=headers)

    # Converts the response to JSON to make it easy to pull specific results
    response = json.loads(response_raw.text)

    # If there is a key name "data" that means there are results
    if "data" in response:
        counter += 1
        # Loop through the results and append to all_requests
        for request in response['data']:
            all_requests.append(request)

        # Check to see if the next URI is blank, if it is we are done pulling 
        # results
        next_url = response['next']['uri']
        if next_url == '':
            # Break out of the loop
            break
        # If there is a next uri build the URL for the next loop through
        url = api_host + next_url
    else:
        # If data is not in the response then there are no results. This means
        # that we can finish the loop
        if first:
            first = False

# Check to see if we should print as a Single JSON Object or one JSON entry per
# new line in the log file.
if single_object:
    # Set a variable to a new Dictionary to build the new structure of 
    # {"data": []}
    output_requests = {"data": all_requests}
    if pretty:
        msg = prettyJson(output_requests)
    else:
        msg = json.dumps(output_requests)
    # Send the result to the log file
    logOut(msg)
else:
    # Since we are printing each request as a single JSON per line loop through
    # all of the requests and log out individually
    for curRequest in all_requests:
        if pretty:
            msg = prettyJson(curRequest)
        else:
            msg = json.dumps(curRequest)
        # Send the result to the log file
        logOut(msg)