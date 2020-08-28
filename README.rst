========
IDEM_LXD
========

WORK IN PROGRESS!!  You have been warned.

This is a module for the idem project to allow for managing containers on LXD.


This module depends on idem and pylxd.

Usage:

* Set up LXD on a Linux system.
   https://lxd.readthedocs.io/en/latest/#installing-lxd-from-packages

* Configure the LXD daemon to allow external connections over the rest API.
   https://ubuntu.com/blog/directly-interacting-with-the-lxd-api

* Install idem

.. code-block:: bash

    pip install idem

* Install this repo

.. code-block:: bash

    pip install this repo

* Create certs for a secure connection

.. code-block:: bash

    mkdir ~/lxd
    cd ~/lxd
    openssl req -newkey rsa:2048 -nodes -keyout lxd.key -out lxd.csr
    openssl x509 -signkey lxd.key -in lxd.csr -req -days 365 -out lxd.crt

* Idem uses the `acct` project to securely store credentials. Let's create a
  credentials file. This can be anywhere, but let's put it in the root of your
  home directory for now. `~/demo_config.yaml`

.. code-block:: json

    lxd.client:
      default:
        endpoint: https://localhost:8443
        password: <password>
        cert: /home/boucha/lxd/lxd.crt
        key: /home/boucha/lxd/lxd.key
        verify: False


* Now let's use the `acct` tool to encrypt our creds file.

.. code-block:: bash

    $ acct ~/demo_config.yaml

    New encrypted file created at: /home/boucha/demo_config.yaml.fernet
    The file was encrypted with this key:
    307GR-MdzJuT33rP10vrbZp1Z9Z2g-jIa19T42fVMUY=


Take note of the encryption key and store it in a password safe like 1password
or bitwarden. Also notice that a new file was created that has a `.fernet`
suffix. This `.fernet` file is what we'll keep around. You can move or delete
the `demo_config.yaml` if you want to keep your password secure.

* Now let's set up some environment variables so idem can find your creds. Use
  the encrypted key above for the `ACCT_KEY` value below

.. code-block:: bash

    export ACCT_FILE=/home/boucha/repos/demo_config.yaml.fernet
    export ACCT_KEY="JyM-E32J4Mnpiwwq6ZK333MmYEGiGmhDOGY2x8u0="

1. Now you should be able to run idem commands on your system

.. code-block:: bash

    idem exec lxd.containers.list


Currently I've only added modules to do some basic management of containers and
images.


tips
====

During testing and development if you leave your `~/demo_config.yaml` you can
edit the file and re-encrypt the file easily with the following command.

.. code-block:: bash

    acct --acct-key=$ACCT_KEY demo_config.yaml
