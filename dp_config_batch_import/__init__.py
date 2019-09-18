import argparse
import base64
import requests
import urllib3


# Disable warnings, as XML Mgmt often has a self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def run_with_args(args):
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
