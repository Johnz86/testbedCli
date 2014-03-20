"""Testbed Manager.

Usage:
  testbed PROFILE (status|start|stop|kill|enable|disable|create|destroy)
  testbed PROFILE (backup|restore|export|import) [LABEL]
  testbed PROFILE (delete|archive) (export|backup) [LABEL]
  testbed PROFILE (install|update) [NODE]
  testbed list (installers|profiles|setup|status)
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

@cli.command({'PROFILE':str,'status':True})
def status(arguments):
    print arguments
    
@cli.command({'PROFILE':str,'start':True})
def start(arguments):
    print arguments
    
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
    
@cli.command({'list':True,'installers':True})
def list_installers(arguments):
    print arguments
    
@cli.command({'list':True,'profiles':True})
def list_profiles(arguments):
    profile_list = Profiles.load_profile_list(os.path.join(env.path, "resourceCache.pickle"))
    Display.print_list_table("Profile list",profile_list)

@cli.command({'list':True,'setup':True})
def list_setup(arguments):
    Display.print_key_value_table(env.properties)
    
@cli.command({'list':True,'status':True})
def list_status(arguments):
    print arguments