"""
Created on 24.3.2013
@author: Jan Jakubcik
@description: Includes all functions, that use networking.
"""

from sys import platform
import subprocess
import logging

class ServerList:
    def __init__(self, host_list = []):
        self.operating_system = "windows" if "win" in platform.lower() else "linux"
        self.server_list = host_list

    def set_host_list(self, host_list):
        self.server_list = host_list

    def get_host_list(self):
        return self.server_list

    def add_host(self, hostname):
        self.server_list.append(hostname)

    def ping_all_hosts(self):
        """Send ping for status of all server in provided list."""
        logging.info("Get status of {0} servers.".format(self.server_list))
        if not len(self.server_list):
            raise ValueError, "List of servers is empty."
        for host in self.server_list:
            logging.info(self.ping_host(host))

    def ping_host(self, host, count = "1"):
        """This execute function should ping server under windows platform"""
        ping_count_argument = "-n" if self.operating_system == "windows" else "-c"
        result = subprocess.Popen(["ping", ping_count_argument,count,host], shell=False, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout, stderr = result.communicate()
        if "unreachable" in stdout.lower():
            return 'Server %s is down.' % (host)
        elif result.returncode == 0:
            return 'Server %s is up.' % (host)
        elif "Request timed out." in stdout:
            return self.ping_host(count, host)
        else:
            return 'Server %s is down.' % (host)
