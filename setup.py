from setuptools import setup

version = {}
with open('./dp_config_batch_import/version.py') as fp:
    exec(fp.read(), version)

setup(
    name='dp_config_batch_import',
    version=version['__version__'],
    description='Batch import configuration packages to IBM DataPower Gateway.',
    url='https://github.com/IBM/dp-config-batch-import',
    author='Aidan Harbison',
    author_email='aharbis@us.ibm.com',
    license='MIT',
    packages=[
        'dp_config_batch_import'
    ],
    entry_points={
        'console_scripts': [
            'dp-config-batch-import=dp_config_batch_import.command_line:main'
        ]
    },
    install_requires=[
        'requests'
    ],
    zip_safe=False
)
