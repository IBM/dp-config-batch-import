import dp_config_batch_import

import argparse


def get_version():
    version = {}
    with open('./dp_config_batch_import/version.py') as fp:
        exec(fp.read(), version)
    version_str = 'v{}'.format(version['__version__'])
    return version_str


def process_args():
    argparser = argparse.ArgumentParser(description='Batch import configuration packages to IBM DataPower Gateway via XML Management Interface.')
    argparser.add_argument('hostname', type=str, nargs=1, help='hostname of DataPower Gateway')
    argparser.add_argument('domain', type=str, nargs=1, help='target application domain')
    argparser.add_argument('-P', '--port', type=int, nargs=1, help='xml-mgmt port, default: 5550')
    argparser.add_argument('-u', '--user', type=str, nargs=1, help='username, default: admin')
    argparser.add_argument('-p', '--password', type=str, nargs=1, help='password, default: admin')
    argparser.add_argument('-V', '--verbose', action='store_true', help='verbose output')
    argparser.add_argument('-v', '--version', action='version', version=get_version())
    argparser.add_argument('export', type=str, nargs='+', help='export package(s) to push, should be ZIP archives')
    args = argparser.parse_args()
    return args


def main():
    args = process_args()
    dp_config_batch_import.run_with_args(args)


if __name__ == '__main__':
    main()
