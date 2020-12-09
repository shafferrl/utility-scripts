"""
Opens access log file and parses, checking each IP address against 
database to save location and other relevant information.

"""

# Relevant library imports
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json, ssl, datetime, re

# Specify file to parse
filename = 'access_logs_20191211.txt'
ip_dict = {}

# Open log file, find all log entries, and save to dictionary with each IP address as unique key
with open(filename) as log_file:
    log_count = 0
    for log in log_file:
        try:
            log_entry = re.findall('^(\S+)\s?-\s-\s([\S\s]+$)', log)[0]
            ip_dict[log_entry[0]] = ip_dict.get(log_entry[0], []) + [log_entry[1]]
            log_count += 1
        except IndexError: pass
    print('Total # Requests: ', log_count)
    print('Unique IP Addresses: ', len(ip_dict))

# Set SSL/TLS encryption parameters
ctx = ssl.create_default_context()
ctx.check_hostname = True
ctx.verify_mode = ssl.CERT_REQUIRED

# Loop through all IP addresses and find metadata on each as available
for ip_index, log_ip in enumerate(ip_dict):
    ip_dict[log_ip] = {
        'noRequests': str(len(ip_dict[log_ip])),
        'requests': ip_dict[log_ip],
        'urlError': []
    }
    # Obtain some metadata on IP address through free API
    try:
        jsobject = urlopen('http://api.db-ip.com/v2/free/'+log_ip).read().decode()
        log_ip_dict = json.loads(jsobject)
        ip_dict[log_ip].update(log_ip_dict)
    except:
        ip_dict[log_ip]['urlError'].append('http://api.db-ip.com/v2/free/')

    # Scrape from website metadata that can't be obtained from API
    try:
        # Set user agent to keep from getting blocked
        header = {'User-Agent': 'Mozilla/5.0'}
        # Set up request
        url = 'https://db-ip.com/' + log_ip
        req = Request(url, headers=header)
        # Scrape data from page and parse with BeautifulSoup
        html = urlopen(req, context=ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        # Attempt to get hostname information for IP address
        try:
            host_name = soup(string='ISP')[0].parent.next_sibling.string
        except:
            host_name = 'N/A'
        # Attempt to get location information for IP address
        try:
            lat_long = soup(string='Coordinates')[0].parent.next_sibling.string
            location = {
                'lat': lat_long.split(',')[0].strip(),
                'lng': lat_long.split(',')[1].strip()
            }
        except:
            location = 'N/A'
        # Add newly gathered information to dictionary
        ip_dict[log_ip].update({'hostName': host_name, 'location': location})
    except:
        ip_dict[log_ip]['urlError'].append('https://db-ip.com/')
    print(f'IP Address #{ip_index} complete')
        
# Set timestamp and prefix from which to name output file
timestamp = '-'.join('_'.join(''.join(datetime.datetime.today().__str__().split('-')).split()).split(':'))[:17]
out_file_prefix = 'ip_access_info'

# Open and write to output file
with open(out_file_prefix + '_' + timestamp + '.txt', 'w') as output_file:
    output_file.write('{\n')
    for ip_entry in ip_dict:
        output_file.write('"'+ip_entry+'":\n'+str(json.dumps(ip_dict[ip_entry], indent=4))+',\n')
    output_file.write('}')
