import dp_config_batch_import

import argparse

def get_version():
    version = {}
    with open('./dp_config_batch_import/version.py') as fp:
        exec(fp.read(), version)
    version_str = 'v{}'.format(version['__version__'])
    return version_str

def process_args():
    argparser = argparse.ArgumentParser(description='Imports configuration exports to a DataPower via xml-mgmt.')
    argparser.add_argument('-D', '--datapower', type=str, nargs=1, help='DataPower hostname to push to')
    argparser.add_argument('-d', '--domain', type=str, nargs=1, help='Destination domain')
    argparser.add_argument('-P', '--port', type=int, nargs=1, help='Overrides default xml-mgmt port: 5550')
    argparser.add_argument('-u', '--user', type=str, nargs=1, help='Overrides default user: admin')
    argparser.add_argument('-p', '--password', type=str, nargs=1, help='Overrides default password: admin')
    argparser.add_argument('-v', '--verbose', action='store_true', help='Verbose output.')
    argparser.add_argument('export', type=str, nargs='+', help='Export file(s) to push.')
    args = argparser.parse_args()
    return args


def main():
    args = process_args()
    dp_config_batch_import.run_with_args(args)


if __name__ == '__main__':
    main()
