#!/usr/bin/python3


# cycle a POE port in meraki

import requests
import argparse
import json
import os

token = os.getenv("MERAKI_API_KEY")
pippo = os.getenv("pippo")

if  token == None:
	print("MERAKI_API_KEY is not defined")
	exit(5)
	

argParser = argparse.ArgumentParser()
# argParser.add_argument("-o", "--org", required=True, help="meraki org")
argParser.add_argument("-n", "--net", required=True, help="meraki network")
argParser.add_argument("-s", "--serial", required=True, help="ap serial")

args = argParser.parse_args()

# print("Org:"+args.org);
print("Network:"+args.net);
print("Serial:"+args.serial);
print("Pippo:"+pippo);

topo_url = "https://api.meraki.com/api/v1/networks/"+args.net+"/topology/linkLayer"
payload = None
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token
}

print("Fetching network topology for:"+args.net) 
response = requests.request('GET', topo_url, headers=headers, data = payload)
# print(response.text)
 
# returns JSON object as
# a dictionary
data = json.loads(response.text)

lookfor=args.serial

# Iterating through the json
# list
conn=False
found=False
found_port=False
found_switch=False


for link in data['links']:
	left=link['ends'][0]
	right=link['ends'][1]

	if left['device']['serial'] == lookfor:
		found=left
		conn=right
	if right['device']['serial'] == lookfor:
		found=right
		conn=left

if found != False:
	# DEVICE: {'node': {'derivedId': '247165646677235', 'type': 'device'}, 'device': {'serial': 'AAAA-BBB-CCCC, 'name': 'def'}, 'discovered': {'lldp': {'portId': '0', 'portDescription': 'eth0'}, 'cdp': None}}
	# CONNECTS TO: {'node': {'derivedId': '114598823386502', 'type': 'device'}, 'device': {'serial': 'EEEE-FFFF-DDDD', 'name': 'abc'}, 'discovered': {'lldp': {'portId': '3', 'portDescription': 'Port 3'}, 'cdp': None}}

	print("DEVICE:",found)	
	print("CONNECTS TO:",conn)	

	print("Switch serial: "+conn['device']['serial'])
	print("Switch port: "+conn['discovered']['lldp']['portId'])

	found_port=conn['discovered']['lldp']['portId']
	found_switch=conn['device']['serial']

	if found_switch != False and found_port != False:
		print("Cycling POE port "+found_port+" on switch "+found_switch)
		dict={}
		dict['ports']=[ found_port ]

		payload=json.dumps(dict)
	
		poe_url = f"https://api.meraki.com/api/v1/devices/{found_switch}/switch/ports/cycle"
		headers = {
    			"Content-Type": "application/json",
    			"Accept": "application/json",
    			"Authorization": "Bearer " + token
		}

		print(poe_url)
		print(payload)
		# response = requests.request('POST', poe_url, headers=headers, data = payload)
		# print(response.text.encode('utf8'))
	
