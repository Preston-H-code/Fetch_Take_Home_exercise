import json
import threading
import yaml
import requests
import time
import os
from datetime import datetime
from collections import defaultdict


# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

#ensure even endpoint has a Name and Url
def is_config_valid(config):
    for endpoint in config:
        if endpoint.get('url') is None:
            print("Invalid endpoint Missing a url at Endpoint: "+str(endpoint))
            return False
        if endpoint.get('name') is None:
            print("Invalid endpoint Missing a Name at Endpoint: " + str(endpoint))
            return False
    return True

#Verifies if the file is a YAML
def is_file_yaml(file_path):
    if file_path.lower().endswith('.yaml') or file_path.lower().endswith('.yml'):
        return True
    else:
        raise Exception("Invalid file format: " + file_path +" use a yaml file.")

#Verfies the file exist and is not a directory
def does_file_exist(file_path):
    return os.path.isfile(file_path)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method') or "GET"
    headers = endpoint.get('headers')
    body = endpoint.get('body')
    if body is not None:
        body = json.loads(endpoint.get('body'))
    try:
        response = requests.request(method, url, headers=headers, json=body,timeout=.5)
        if 200 <= response.status_code < 300:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path,cycle):
    config = file_path
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    print(f"Monitoring Cycle # {cycle} Started at:  {datetime.now().strftime("%H:%M:%S %m-%d-%Y")}")
    for endpoint in config:
        #Removes protocal, page path, and ports leaving just domain and subdomain
        full_domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0].split(".")
        #removes the subdomains and returns just the domain
        domain = full_domain[-1] if len(full_domain) == 1 else full_domain[-2]+"."+full_domain[-1]
        result = check_health(endpoint)

        domain_stats[domain]["total"] += 1
        if result == "UP":
            domain_stats[domain]["up"] += 1
    # Log cumulative availability percentages
    print("---")
    print(f"Cycle # {cycle} Results: ")
    for domain, stats in domain_stats.items():
        availability = round(100 * stats["up"] / stats["total"])
        print(f"{domain} has {availability}% availability percentage")

    print(f"The Cycle {cycle} completed {datetime.now().strftime("%H:%M:%S %m-%d-%Y")}")
    print("---")

def run_monitor(endpoints, count):
    threading.Thread(target=monitor_endpoints,args=(endpoints,count)).start()

# Entry point of the program
if __name__ == "__main__":

    import sys
    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        does_file_exist(config_file)
        is_file_yaml(config_file)
        yml_config = load_config(config_file)
        if is_config_valid (yml_config):
            counter = 0
            while True:
                counter = counter + 1
                run_monitor(yml_config, counter)
                time.sleep(15)
        print("Fix your yaml file. Every endpoint needs a name and url.")
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except FileNotFoundError:
            print(f"File {config_file} not found. Please check the path and try again.")
    except Exception as error:
        print(error)
