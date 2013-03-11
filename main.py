#!/usr/bin/python
# Jabber translate service
#
# License: GPL-v3
#
import ConfigParser
import sys
import logging
import argparse

from twisted.internet import reactor

from jtranslate import jtranslateComponent

logging.getLogger().setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('path', help='Path to the configuration file')

def main(conf):
    version = '0.0'
    config = ConfigParser.ConfigParser()
    config.read(conf)
    try:
        jid = config.get('component', 'jid')
        password = config.get('component', 'password')
        host = config.get('component', 'host')
        port = config.get('component', 'port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        logging.error('Wrong configuration file')
        sys.exit(1)
    c = jtranslateComponent(version, jid, config)
    c.connect(port, password, host)
    reactor.run() 

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.path)
