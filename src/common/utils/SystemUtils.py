"""
Created on 19.9.2013
@author: Jan Jakubcik
@description: Includes all functions, that manipulate filesystem.
"""

import os
import sys
import shlex
import shutil
import subprocess
import tempfile
import logging
import time
import string
import fnmatch
from common.Config import *

def parent_dir(file_path):
    """get parent dir of the file"""
    return os.path.dirname(os.path.abspath(file_path))
 
def create_dir(folder_name):
    """create directory and return path"""
    if os.path.isdir(folder_name):
        logging.info('Folder {0} exists'.format(folder_name))
    else:
        logging.info('Creating folder {0}'.format(folder_name))
        os.mkdir(folder_name)
    return folder_name

def verify_destination_and_target_path(destination, target):
    """Verify if target and destination folder exists."""
    if not os.path.isdir(destination):
        logging.error("Destination folder {0} does not exist !".format(destination))
        sys.exit(1)
    if not os.path.isdir(target):
        logging.error("Target folder {0} does not exist !".format(target))
        sys.exit(1)

def move_file_type_from_folder(folder, destination, file_type):
    """Move files from folder to other folder."""
    logging.info('Moving files from folder {0}'.format(folder))
    for file in folder:
        if file.endswith(file_type):
                logging.info('Moving file {0} to {1}'.format(file,destination))
                shutil.move(folder,destination)

def move_path_to_folder(target_path, destination_folder):
    """Move target file to destination folder."""
    logging.info('Moving target {0} to destination {1}'.format(target_path, destination_folder))
    if os.path.exists(target_path):
        shutil.move(target_path, destination_folder)
    else:
        logging.error('Target path {0} dose not exist'.format(target_path))

def copy_path_to_folder(target_path, destination_folder):
    """Copy target file to destination folder."""
    logging.info('Copy target {0} to folder {1}'.format(target_path, destination_folder))
    if os.path.exists(target_path):
        shutil.copy(target_path, destination_folder)
    else:
        logging.error('Target path {0} dose not exist'.format(target_path))

def get_temp_folder():
    """
    Temp Folder gets folder in following logic.
    The directory named by the TMPDIR environment variable.
    The directory named by the TEMP environment variable.
    The directory named by the TMP environment variable.
    A platform-specific location:
    On RiscOS, the directory named by the Wimp$ScrapDir environment variable.
    On Windows, the directories C:\TEMP, C:\TMP, \TEMP, and \TMP, in that order.
    On all other platforms, the directories /tmp, /var/tmp, and /usr/tmp, in that order.
    As a last resort, the current working directory.
    """
    temp_folder = create_dir(os.path.join(tempfile.gettempdir(),"ciBuilder.{0}".format(str(time.time())) ))
    return temp_folder

def remove_dir(folder_path):
    if os.path.exists(folder_path):
        logging.info('Remove folder {0}'.format(folder_path))
        shutil.rmtree(folder_path)

def remove_files_in_dir(folder_path, file_type="*"):
    """
    Remove files in target directory.
    @param folder_path: Path to folder. If it is not a folder log an error.
    @param file_type: Type off files, that should be removed. Default value is *. Example: *.txt, *.rpm
    """
    if os.path.isdir(folder_path):
        execute_command('rm -r {0}'.format(os.path.join(folder_path, file_type)))
    else:
        logging.error('Path {0} is not a directory'.format(folder_path))

def get_dirs_in_folder(path):
    """Returns the list of all folders in target directory"""
    return [ name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name)) ]

def get_spec_from_folder(path):
    """Return spec file from directory."""
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, "*.spec"):
                return os.path.join(root, name)
    return "None *.spec file"

def list_files_in_folder(path):
    """Returns the list of all files in target directory"""
    return [ name for name in os.listdir(path) if os.path.isfile(os.path.join(path,name)) ]

def shell_exec(command):
    """
    execute system command and return exit code with std err and std out
    in case that command is invalid, exit code 99 is returned
    """
    logging.info("command:"+command)
    return_code = 0
    std_out = ""
    try:
       args = shlex.split(command)
       process = subprocess.Popen(args,shell=False,stdin=None,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
       while True:
           line_out = process.stdout.readline()
           if line_out == "":
              break
           std_out = std_out + line_out
       process.wait()
       return_code = process.returncode
       std_out = string.strip(std_out)
    except OSError:
       return_code = 99
    return return_code, std_out

def execute_command(command, error_message="command failed !"):
    return_code, std_out = shell_exec(command)
    if return_code != 0:
        logging.error(error_message)
        logging.error(std_out)
        sys.exit(1)
    else:
        logging.info(std_out)

