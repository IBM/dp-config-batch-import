#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import base64
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

argparser = argparse.ArgumentParser(description='Imports configuration exports to a DataPower via xml-mgmt.')
argparser.add_argument('-D', '--datapower', type=str, nargs=1, help='DataPower hostname to push to')
argparser.add_argument('-d', '--domain', type=str, nargs=1, help='Destination domain')
argparser.add_argument('-P', '--port', type=int, nargs=1, help='Overrides default xml-mgmt port: 5550')
argparser.add_argument('-u', '--user', type=str, nargs=1, help='Overrides default user: admin')
argparser.add_argument('-p', '--password', type=str, nargs=1, help='Overrides default password: admin')
argparser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
argparser.add_argument('export', type=str, nargs='+', help='Export file(s) to push.')
args = argparser.parse_args()
if args.verbose:
	print(args)

datapower = args.datapower[0]
domain = args.domain[0]
if args.user is not None:
	user = args.user[0]
else:
	user = 'admin'
if args.password is not None:
	password = args.password[0]
else:
	password = 'admin'
if args.port is not None:
	port = str(args.port[0])
else:
	port = '5550'
url = 'https://' + datapower + ':' + port + '/'
if args.verbose:
	print('User:', user)
	print('Password:', password)
	print('URL:', url)

soap_env_head = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">'
soap_env_tail = '</soapenv:Envelope>'
soap_body_head = '<soapenv:Body>'
soap_body_tail = '</soapenv:Body>'
dp_req_head = '<dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="' + domain + '">'
dp_req_tail = '</dp:request>'
dp_do_import_head = '<dp:do-import source-type="ZIP" dry-run="false" overwrite-objects="false" overwrite-files="false">'
dp_do_import_tail = '</dp:do-import>'
dp_input_file_head = '<dp:input-file>'
dp_input_file_tail = '</dp:input-file>'

def build_xml(data):
	print('Building XML')
	return soap_env_head + soap_body_head + dp_req_head + \
	 	   dp_do_import_head + dp_input_file_head + \
	 	   base64.b64encode(data).decode('ascii') + \
	 	   dp_input_file_tail + dp_do_import_tail + \
			 dp_req_tail + soap_body_tail + soap_env_tail

print('Domain: ' + domain)
for filename in args.export:
	print('Preparing to import: ' + filename)
	with open(filename, 'rb') as lines:
		data = lines.read()
	xml = build_xml(data)
	if args.verbose:
		print('XML:', xml)
	print('Sending POST')
	r = requests.post(url, auth=(user, password), data=xml, verify=False)
	if r.status_code == 200:
		print('File uploaded successfully')
		if args.verbose:
			print(r.text)
	else:
		print('File upload failed:')
		print(r.text)
		exit()
