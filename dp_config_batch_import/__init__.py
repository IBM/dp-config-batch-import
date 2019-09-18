import argparse
import base64
import requests
import urllib3
import re
import xml.dom.minidom

# Disable warnings, as XML Mgmt often has a self-signed certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global for verbose logging, set via --verbose argument
VERBOSE = False


def get_user(args):
    if args.user is not None:
        user = args.user[0]
    else:
        user = 'admin'
    return user


def get_password(args):
    if args.password is not None:
        password = args.password[0]
    else:
        password = 'admin'
    return password


def get_port(args):
    if args.port is not None:
        port = str(args.port[0])
    else:
        port = '5550'
    return port


def build_url(hostname, port):
    url = 'https://' + hostname + ':' + port + '/'
    if VERBOSE:
        print('URL:', url)
    return url


def print_pretty_xml(xml_str):
    dom = xml.dom.minidom.parseString(xml_str)
    dom_pretty = dom.toprettyxml()
    print(dom_pretty)


def build_xml(domain, data):
    file_content = base64.b64encode(data).decode('ascii')
    xml_template = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                        <soapenv:Body>
                              <dp:request xmlns:dp="http://www.datapower.com/schemas/management" domain="{}">
                                  <dp:do-import source-type="ZIP" dry-run="false" overwrite-objects="false" overwrite-files="false">
                                      <dp:input-file>{}</dp:input-file>
                                  </dp:do-import>
                              </dp:request>
                          </soapenv:Body>
                      </soapenv:Envelope>'''
    xmlRequestStr = xml_template.format(domain, file_content).replace('\n', '')
    xmlRequest = re.sub(r'> +<', '><', xmlRequestStr)
    if VERBOSE:
        print('Generated XML:\n')
        print_pretty_xml(xmlRequest)
    return xmlRequest


def process_file(filename, domain, url, user, password):
    print('Preparing to import: ' + filename)
    with open(filename, 'rb') as lines:
        data = lines.read()
    xml = build_xml(domain, data)
    if VERBOSE:
        print('Sending POST request')
    r = requests.post(url, auth=(user, password), data=xml, verify=False)
    if r.status_code == 200:
        print('File uploaded successfully')
        if VERBOSE:
            print(r.text)
    else:
        print('File upload failed:')
        print(r.text)
        exit()


def run_with_args(args):
    if args.verbose:
        global VERBOSE
        VERBOSE = True
        print(args)
    domain = args.domain[0]
    hostname = args.hostname[0]
    port = get_port(args)
    url = build_url(hostname, port)
    user = get_user(args)
    password = get_password(args)
    if VERBOSE:
        print('Target application domain: ' + domain)
    for filename in args.export:
        process_file(filename, domain, url, user, password)
