"""Testbed Manager.

Usage:
  testbed list (installers|profiles|setup|status)
  testbed PROFILE (status|start|stop|kill|enable|disable|create|destroy)
  testbed PROFILE (backup|restore|export|import) [LABEL]
  testbed PROFILE (delete|archive) (export|backup) [LABEL]
  testbed PROFILE (install|update) [NODE]
  testbed (-h | --help)
  testbed --version

Arguments:
  PROFILE      absolute path to profile
  LABEL        name of backup file
  NODE     name of the node (ADM|PGW|NDS)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os.path
import logging
from common.utils import NetworkUtils
import common.utils.DisplayUtils as Display
from common.profiles import Profiles
from datetime import datetime
from environment import env
from libs.clicommand import Cli
from libs.docopt import docopt

__version__ = '0.3'

start_time = datetime.now()

def OnStart():
    env.load_properties()

def OnExit():
    stop_time = datetime.now()
    duration = stop_time - start_time
    logging.info("Command duration: " + str(duration))

if __name__ == '__main__':
    cli = Cli(docopt(__doc__, version="Testbed Command Line Interface 0.3"))
    cli.on_start = lambda:OnStart()
    cli.on_exit = lambda:OnExit()

@cli.command({'list':True,'installers':True})
def list_installers(arguments):
    print arguments

@cli.command({'list':True,'profiles':True})
def list_profiles(arguments):
    profile_list = Profiles.load_profile_list(os.path.join(env.path, "resourceCache.pickle"))
    Display.print_table_list("Profile list",profile_list)

@cli.command({'list':True,'setup':True})
def list_setup(arguments):
    Display.print_table_key_value(env.properties)

@cli.command({'list':True,'status':True})
def list_status(arguments):
    #discover the list of these servers.
    servers = NetworkUtils.ServerList(["10.66.1-22.254","10.66.40.254","10.66.50.254"])
    #execute nmap with custom arguments (execute only ping and resolve hostname)
    servers.execute_nmap(['-sP', '-R'])
    servers.print_status()

@cli.command({'PROFILE':str,'status':True})
def status(arguments):
    profile = Profiles.TestbedProfile(arguments['PROFILE'])
    servers = NetworkUtils.ServerList(profile.get_all_hostnames())
    servers.execute_nmap()
    servers.print_status()

@cli.command({'PROFILE':str,'start':True})
def start(arguments):
    profile = Profiles.TestbedProfile(arguments['PROFILE'])
    for host in profile.get_all_hostnames():
        NetworkUtils.ssh_command(profile.get_vm_host(), "xm start {0}".format(host))

@cli.command({'PROFILE':str,'stop':True})
def stop(arguments):
    print arguments

@cli.command({'PROFILE':str,'kill':True})
def kill(arguments):
    print arguments

@cli.command({'PROFILE':str,'enable':True})
def enable(arguments):
    print arguments

@cli.command({'PROFILE':str,'disable':True})
def disable(arguments):
    print arguments

@cli.command({'PROFILE':str,'create':True})
def create(arguments):
    print arguments

@cli.command({'PROFILE':str,'destroy':True})
def destroy(arguments):
    print arguments

@cli.command({'PROFILE':str,'backup':True,'LABEL':'?'})
def backup(arguments):
    print arguments

@cli.command({'PROFILE':str,'restore':True,'LABEL':'?'})
def restore(arguments):
    print arguments

@cli.command({'PROFILE':str,'export':True,'LABEL':'?'})
def export(arguments):
    print arguments

@cli.command({'PROFILE':str,'import':True,'LABEL':'?'})
def import_exported(arguments):
    print arguments

@cli.command({'PROFILE':str,'delete':True,'backup':True,'LABEL':'?'})
def delete_backup(arguments):
    print arguments

@cli.command({'PROFILE':str,'delete':True,'export':True,'LABEL':'?'})
def delete_export(arguments):
    print arguments

@cli.command({'PROFILE':str,'archive':True,'backup':True,'LABEL':'?'})
def archive_backup(arguments):
    print arguments

@cli.command({'PROFILE':str,'archive':True,'export':True,'LABEL':'?'})
def archive_export(arguments):
    print arguments

@cli.command({'PROFILE':str,'install':True,'NODE':'?'})
def install_node(arguments):
    print arguments

@cli.command({'PROFILE':str,'update':True,'NODE':'?'})
def update_node(arguments):
    print arguments
