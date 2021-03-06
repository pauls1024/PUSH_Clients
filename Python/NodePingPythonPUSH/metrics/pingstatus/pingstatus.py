#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Pings IPs that are specified and returns 1 if it is up, or 0 if
it is not able to ping. Provide any single IP address (or addresses)
in the IP_ADDRESSES variable below. The program is not asynchronous due
to the restraints of Python 2. More pings will result in a delayed response.
Useful for pinging computers that are hidden behind a firewall.
"""

import socket
import subprocess
from . import config


def is_ipv6(host):
    """
    Checks if address is IPv6, and returns true if matches regex
    """
    try:
        check = bool(socket.inet_pton(socket.AF_INET6, host))
    except socket.error:
        check = False

    return check


def main(system, logger):
    """
    Returns List of IPs in PING_HOSTS and their status (1/0)
    """

    ping_results = {}

    # Windows needs this module for socket to work with Python 2.x
    if system == "Windows":
        import win_inet_pton

    ping_count = config.ping_count
    timeout = config.timeout

    for host in config.ping_hosts:
        if is_ipv6(host):
            if system == "Windows":
                command = "ping -6 -n " + \
                    str(ping_count) + " -w " + \
                    str(timeout) + " " + str(host)
            elif system == "OpenBSD":
                command = "ping6 -c " + \
                    str(ping_count) + " -w " + \
                    str(timeout) + " -q " + str(host)
            else:
                command = "ping6 -c " + \
                    str(ping_count) + " -W " + \
                    str(timeout) + " " + str(host)
        else:  # if address is IPv4
            if system == "Windows":
                command = "ping -n " + \
                    str(ping_count) + " -w " + \
                    str(timeout) + " " + str(host)
            elif system == "OpenBSD":
                command = "ping -c " + \
                    str(ping_count) + " -w " + \
                    str(timeout) + " -q " + str(host)
            else:
                command = "ping -c " + \
                    str(ping_count) + " -W " + \
                    str(timeout) + " " + str(host)

        try:
            # If passes, then ping succeeded
            result = subprocess.check_output(
                command, shell=True, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            result = 0

        # Errors caught by running ping as subprocess convert to 0 for failed ping
        if result != 0:
            result = 1

        ping_results.update({host: result})

    return ping_results
