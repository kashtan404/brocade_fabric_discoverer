brocade_fabric_discoverer
=========

Discover fabrics via brocade network advisor api.

Requirements
------------

Python 3 or higher

python libs:
  - requests
  - json
  - sys
  - getpass
  - re
  - argparse


Usage
------

netadvisor.py [-h] -host HOSTNAME -user USER -pswd PASSWORD

optional arguments:
  - -h, --help            show this help message and exit
  - -host HOSTNAME, --hostname HOSTNAME
                        BNA host
  - -user USER, --user USER
                        BNA user
  - -pswd PASSWORD, --password PASSWORD
                        BNA password


License
-------

MIT

Author Information
------------------

Aleksey Demidov
