# -*- coding: UTF-8 -*-
import sys
import os
import time
import argparse

import config

__author__ = 'Stefan Hechenberger <stefan@nortd.com>'

### Setup Argument Parser
argparser = argparse.ArgumentParser(description='Run DriveboardApp.', prog='driveboardapp')
argparser.add_argument('-v', '--version', action='version', version='%(prog)s ' + config.conf['version'],
                       default=False, help='print version of this app')
argparser.add_argument('-d', '--debug', dest='debug', action='store_true',
                       default=False, help='print more verbose for debugging')
argparser.add_argument('-n', '--nobrowser', dest='nobrowser', action='store_true',
                       default=False, help='do not launch interface in browser')
argparser.add_argument('-c', '--cli', dest='cli', action='store_true',
                       default=False, help='run without server GUI window')
argparser.add_argument('-u', '--usbhack', dest='usbhack', action='store_true',
                       default=False, help='use usb reset hack (advanced)')
argparser.add_argument('--config', dest='config',
                       help='specify alternative configuration')
argparser.add_argument('--list-configs', dest='list_configs', action='store_true',
                       default=False, help='list available configurations')
args = argparser.parse_args()

if args.list_configs:
    config.list_configs()
    sys.exit()

config.conf['usb_reset_hack'] = args.usbhack
config.load(args.config)
# NOTE: web has to be inported before Tkinter is initialized
# otherwise the window will fail open on Windows.
# The config has to be loaded/finalized before importing we
# otherwise some initialization will use the wrong values.
import web

try:
    import tkinter
except ImportError:
    args.cli = True

if not args.cli:
    import window

    root = window.init()

print("DriveboardApp v" + config.conf['version'])

# start server in thread
web.start(browser=(not args.nobrowser), debug=args.debug)

# main thread loop
while 1:
    try:
        if not args.cli:
            try:
                root.update()
            except tkinter.TclError:
                break
        time.sleep(0.1)
    except KeyboardInterrupt:
        break
web.stop()
print("END of DriveboardApp")
