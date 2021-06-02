#!/usr/bin/env python3
""" Implements and demonstrates MessageBird SMS API.

This is compatible only with Python 3.
Usage: python3 mb_sms.py [operation_type] 
Where operation_type is one of: 

balance: Check message balance.
list: List SMS transactions.
send: Sends SMS messages.

"""

import sys
import json
import configparser
import requests


CONFIG_FILE = 'mb_sms.config' # Config file.
URL = "https://rest.messagebird.com/" # Base REST url.
BALANCE_URL = URL+"balance" # Check balance url.
LIST_MSG_URL = URL + "messages" # Retrieve messages list.
SEND_MSG_URL = URL + "messages" # Send messages url.
REST_METHODS = ["balance", "list", "send"] # Supported methods.
g_http_headers = {} # Initialize HTTP Headers with Authorization Key
g_config = configparser.ConfigParser() # Global ConfigParser object.



def read_config():
	""" Read the configuration file and Initialize selected values.
	
	return False if error encountered.
	"""
	try:
		f = open(CONFIG_FILE)
		g_config.read_file(f)
		f.close()
	except Exception as e:
		print(e)
		return False
	
	if(not g_config.has_option('config','key')):
		print("No Access Key defined.")
		return False
	else:
		g_http_headers['Authorization'] = 'AccessKey '+g_config['config']['key']
		return True
	
	
	
	
def print_json(p_json):
	""" Format prints a json.
	
	p_json: The string to format and print.
	"""
	try:
		json_obj = json.loads('['+p_json+']')
		print(json.dumps(json_obj, indent=4))
	except Exception as e:
		print(e.__class__.__name__+': '+str(e))



def check_balance():
	""" Checks balance of the current account.
	"""
	try:
		print(BALANCE_URL)
		r = requests.get(BALANCE_URL, headers=g_http_headers, timeout=10)
		print_json(r.text)
	except Exception as e:
		print(e.__class__.__name__+': '+str(e))



def list_messages():
	""" List messages of this acccount.
	"""
	try:
		r = requests.get(LIST_MSG_URL, headers=g_http_headers, timeout=10)
		print_json(r.text)
	except Exception as e:
		print(e.__class__.__name__+': '+str(e))



def send_message():
	if(not g_config.has_option('config','originator')):
		do_exit("No originator defined")
	if(not g_config.has_option('config','recipients')):
		do_exit("No recipients defined")
	if(not g_config.has_option('config', 'body')):
		do_exit("No content defined")
	
	payload = {'originator': g_config['config']['originator'], 'recipients': g_config['config']['recipients'], 'body': g_config['config']['body']}
	try:
		r = requests.post(SEND_MSG_URL, data=payload, headers=g_http_headers, timeout=10)
		print_json(r.text)
	except Exception as e:
		print(e.__class__.__name__+': '+str(e))



def do_exit(p_msg):
	""" Hard exits the application.
	
	p_msg: Exit message to print.
	"""
	sys.exit(p_msg)



def main(p_method):
	""" Main function.
	"""
	if(read_config() == False):
		do_exit("Config file error.")
		
	if(p_method == "balance"):
		check_balance()
	elif(p_method == "list"):
		list_messages()
	elif(p_method == "send"):
		send_message()
	else:
		pass
	


# Argument parsing
if(len(sys.argv) < 2):
	do_exit("Use argument values: "+str(REST_METHODS))
if(sys.argv[1] not in REST_METHODS):
	do_exit("Use argument values: "+str(REST_METHODS))

main(sys.argv[1])
