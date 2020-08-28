import requests, os, calendar, json, codecs
from datetime import datetime, timedelta

# Initial setup
api_host = 'https://dashboard.signalsciences.net'
email = os.environ.get('SIGSCI_EMAIL') or "user@email.com"
api_token = os.environ.get('SIGSCI_API_TOKEN') or "REPLACE_ME"
corp_name = os.environ.get('SIGSCI_CORP') or "REPLACE_ME"
site_name = os.environ.get('SIGSCI_SITE') or "REPLACE_ME"
delta_in_minutes = os.environ.get('SIGSCI_DELTA_IN_MINUTES') or 10
pretty = os.environ.get('SIGSCI_PRETTY') or "false"
single_object = os.environ.get('SIGSCI_SINGLE_OBJECT') or "false"

# log_file for the script
log_file = os.environ.get('SIGSCI_LOG_FILE') or "sigsci_results.json"

if email is None or email == "":
    print("email option is required")
    exit(1)

if api_token is None or api_token == "":
    print("api_token is required")
    exit(1)

if corp_name is None or corp_name == "":
    print("corp_name is required")
    exit(1)

if site_name is None or site_name == "":
    print("site_name is required")
    exit(1)

if delta_in_minutes is None or delta_in_minutes == "":
    delta_in_minutes = 5

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

def logOut(msg):
    if log_file is None or log_file == "":
        print(msg)
    else:
        log = codecs.open(log_file, "a", "utf-8-sig")
        data = "%s" % (msg)
        log.write(data)
        log.write("\n")
        log.close


def prettyJson(data):
    return(json.dumps(data, indent=4, separators=(',', ': ')))

# Calculate UTC timestamps for the previous full hour
# E.g. if now is 9:05 AM UTC, the timestamps will be 8:00 AM and 9:00 AM
until_time = datetime.utcnow() - timedelta(minutes=5)
until_time = until_time.replace(second=0, microsecond=0)
from_time = until_time - timedelta(minutes=int(delta_in_minutes))
until_time = calendar.timegm(until_time.utctimetuple())
from_time = calendar.timegm(from_time.utctimetuple())


# Loop across all the data and output it in one big JSON object
headers = {
    'Content-type': 'application/json',
    'x-api-user': email,
    'x-api-token': api_token
}
url = api_host + ('/api/v0/corps/%s/sites/%s/feed/requests?from=%s&until=%s' % (corp_name, site_name, from_time, until_time))

first = True
counter = 1
all_requests = []

while True:
    page_msg = "Results Page %s" % counter
    print(page_msg)
    #logOut(page_msg)
    response_raw = requests.get(url, headers=headers)
    response = json.loads(response_raw.text)

    if "data" in response:
        counter += 1
        for request in response['data']:
            all_requests.append(request)

        next_url = response['next']['uri']
        if next_url == '':
            break
        url = api_host + next_url

    else:
        if first:
            first = False

if single_object:
    output_requests = {"data": all_requests}
    if pretty:
        msg = prettyJson(output_requests)
    else:
        msg = json.dumps(output_requests)
    #print(msg)
    logOut(msg)
else:
    for curRequest in all_requests:
        if pretty:
            msg = prettyJson(curRequest)
        else:
            msg = json.dumps(curRequest)
        #print(msg)
        logOut(msg)