"""
Created on 24.3.2013
@author: Jan Jakubcik
@description: Includes all functions, that use networking.
"""

from sys import platform
from libs import xmltodict
from environment import env
import subprocess
import logging
import time
import os

class ServerList:
    def __init__(self, host_list = []):
        self.operating_system = "windows" if "win" in platform.lower() else "linux"
        self.server_list = host_list
        self.nmap_result = []

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

    def execute_nmap(self, command_arguments = []):
        """Executes nmap command in linux with the server list. The output is in xml format."""
        xml_result = subprocess.Popen(['nmap', '-oX', '-'] + self.server_list + command_arguments, shell=False, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # get output
        (self._nmap_last_output, nmap_err) = xml_result.communicate()
        # If there was something on stderr, there was a problem so abort...
        if xml_result.returncode != 0:
            raise  ValueError, "Nmap command failed:", nmap_err
        #parse the xml to ordered dict.
        self.nmap_result = xmltodict.parse(self._nmap_last_output)
        return self.nmap_result

    def is_all_up(self):
        """If the number of up servers is the same as the total number of servers report that all are up."""
        if self.nmap_result["runstats"]["host"]["@up"] == self.nmap_result["runstats"]["host"]["@total"]:
            return True
        else:
            return False

    def is_all_down(self):
        """If the number of up servers is the same as the total number of servers report that all are up."""
        if self.nmap_result["runstats"]["host"]["@down"] == self.nmap_result["runstats"]["host"]["@total"]:
            return True
        else:
            return False

    def print_status(self):
        for host in self.nmap_result['nmaprun']['host']:
            logging.info("Server {0} is {1}".format(host["hostnames"]["hostname"]["@name"], host["status"]["@state"]))

    def execute_nmap_until(self, condition):
        """list the status of servers until condition is fulfilled"""
        while True:
            self.execute_nmap()
            self.print_status()
            if condition:
                break
            else:
                time.sleep(10)
                self.execute_nmap()

def get_private_key(file_path = ""):
    ssh_key_file = env.get_property("SSH_KEY_PRIVATE")
    if os.path.isfile(ssh_key_file):
        return os.path.abspath(ssh_key_file)
    else:
        key_file_in_env_foldder = os.path.join(env.path,ssh_key_file)
        return key_file_in_env_foldder if os.path.isfile(key_file_in_env_foldder) else None

def ssh_command(server, command):
    """executes command with ssh on remote machine"""
    ssh_key = get_private_key()
    ssh_options = env.get_property("SSH_OPTIONS")
    command = "ssh -i {0} {1} root@{2} '{3}' ".format(ssh_key,ssh_options,server,command)
    print command