# dp-config-batch-import

Batch import configuration packages to IBM DataPower Gateway.

![GitHub release](https://img.shields.io/github/release/IBM/dp-config-batch-import)
![GitHub](https://img.shields.io/github/license/IBM/dp-config-batch-import)

## Pre-requisites

### XML Management Interface

Since this script is designed to upload files via the [XML management interface](https://www.ibm.com/support/knowledgecenter/SS9H2Y_7.7.0/com.ibm.dp.doc/networkaccess_xmi.html) the `xml-mgmt` object must be enabled and up in the `default` domain of the gateway you wish to target. You can validate this easily by logging into the CLI of the gateway and checking as follows:

```
idg# show xml-mgmt

xml-mgmt [up]
--------
 admin-state enabled
 ip-address 0.0.0.0
 port 5550
 acl xml-mgmt  [up]
 slm-peering 10 Seconds
 mode any+soma+v2004+amp+slm+wsrr-subscription
 ssl-config-type server
```

## Installation

1. Clone, fork, or download the repository

    ```bash
    $ git clone git@github.com:IBM/dp-config-batch-import.git
    $ cd dp-config-batch-import/
    ```

2. Install package via `pip3`

    ```bash
    $ pip3 install .
    ```

    Note: Installing via `pip3` adds the `dp-config-batch-import` executable to your PATH.

3. Validate the installation

    ```bash
    $ dp-config-batch-import --version
    ```

## Usage

This script can be used to import a single configuration package, or multiple packages, to a target DataPower Gateway application domain. You control the behavior of the script through command-line arguments. The minimum usage would be as follows:

```bash
$ dp-config-batch-import my.datapower.com my_domain export.zip
```

This would import the configuration package `export.zip` into the `my_domain` application domain on the DataPower Gateway at hostname `my.datapower.com`.

Since no other arguments were provided, some defaults were used:

- `user` defaults to `admin`
- `password` defaults to `admin`
- `port` defaults to `5550`

You can specify each of these via command-line argument. For example:

```bash
$ dp-config-batch-import \
    --user "myaccount" \
    --password "mypassword" \
    --port 9550 \
    my.datapower.com my_domain export.zip
```

You can also import / deploy multiple configuration packages at once, using either wildcards or specifying multiple filenames manually.

```bash
# using wildcards
$ dp-config-batch-import my.datapower.com my_domain export_*.zip

# specifying each manually
$ dp-config-batch-import my.datapower.com my_domain export_1.zip export_2.zip export_3.zip
```

## Troubleshooting

You can enable verbose output via the `-V, --verbose` command line argument to get a little more detail from the script as it runs. If this does not help to solve your problem, please feel free to [open an issue](https://github.com/IBM/dp-config-batch-import/issues/new).
