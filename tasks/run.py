import os, sys, requests, json
import urllib3
import logging
from google.cloud import logging

# disable insecure SSL certificate warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# add your Toggl API Token
API_TOKEN = "123456789"

def write_log(msg):
    logging_client = logging.Client()
    logger = logging_client.logger('time-tracker-log')
    logger.log_text(msg, severity='INFO')

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        #print("all good")
        return True
    except requests.ConnectionError:
        print("no Internet connection")
    return False


def start_time_entry():
    if not check_internet():
        write_log("Internet down, was trying to start time tracking")
        return "Backend Is Unreachable", 523
    
    url = 'https://www.toggl.com/api/v8/time_entries/start'

    #-- edit your workspace and project IDs
    payload = {"time_entry":{"wid":123456789,"pid":123456789,"created_with":"curl"}}
    #--

    x = requests.post(url, json = payload, auth = (API_TOKEN, 'api_token'), verify=False)
    parsed = json.loads(x.text)
    id_raw = parsed["data"]["id"]
    id = str(id_raw)

    write_log("started time entry with ID " + id)

    return str(parsed)


def stop_time_entry():
    if not check_internet():
        write_log("Internet down, was trying to start time tracking")
        return "Backend Is Unreachable", 523

    get_id_url = 'https://www.toggl.com/api/v8/time_entries/current'
    x = requests.get(get_id_url, auth = (API_TOKEN, 'api_token'), verify=False)
    get_id_parsed = json.loads(x.text)
    id_raw = get_id_parsed["data"]["id"]
    id = str(id_raw)

    stop_entry_url = 'https://www.toggl.com/api/v8/time_entries/' + id + '/stop'
    y = requests.put(stop_entry_url, auth = (API_TOKEN, 'api_token'), verify=False)
    stop_entry_parsed = json.loads(y.text)

    write_log("stopped time entry with ID " + id)

    return str(stop_entry_parsed)