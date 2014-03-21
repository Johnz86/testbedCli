import os
import pickle
import ConfigParser
import collections
import logging
import pprint
from environment import env

class TestbedProfile:
    def __init__(self, profile_path):
        self.profile_name = os.path.basename(profile_path)
        self.profile_file = get_profile_file_from_path(profile_path)
        self.data = load_profile_from_config(self.profile_file)

    def get_main(self):
        return self.data.get("MAIN","Not Specified.")

    def get_owner(self):
        return self.get_main().get("owner","Not Specified.")

    def get_vm_host(self):
        return self.get_main().get("vmHost","Not Specified.")

    def get_vm_type(self):
        return self.get_main().get("vmType","Not Specified.")

    def get_description(self):
        return self.get_main().get("description","Not Specified.")

    def get_default_java(self):
        return self.get_main().get("java","jre7")

    def get_btrfs_subvolume_path(self):
        return self.get_main().get("tbSubdir",self.profile_name)


def get_profile_file_from_path(profile_path, file_format = ".txt"):
    if (os.path.isfile(profile_path)):
        return os.path.abspath(profile_path)
    elif (os.path.exists(profile_path)):
        return os.path.abspath(os.path.join(profile_path, os.path.basename(profile_path)+file_format))
    else:
        file_path = os.path.abspath(os.path.join(env.properties['PROFILE_HOME'],os.path.join(profile_path, os.path.basename(profile_path)+file_format)))
        if (os.path.exists(file_path)):
            return file_path
        else:
            logging.error("Suggested path {0} does not lead to regular profile. Please provide a path to existing profile.".format(profile_path))
            exit(1)

def load_profile_from_config(profile_path):
    config = ConfigParser.ConfigParser()
    config.read(profile_path)
    return collections.OrderedDict(config._sections)

def load_profile_list(profile_pickle_file):
    if os.path.isfile(profile_pickle_file):
        pickle_data = open(profile_pickle_file,'rb')
        result = pickle.load(pickle_data)
        pickle_data.close()
        return result.getProfiles()
    else:
        logging.error("Failed to load profiles. Cache profile {0} file dose not exist.".format(profile_pickle_file))
        exit(1)

def get_all_profiles(profile_pickle_file):
    profiles = load_profile_list(profile_pickle_file)
    result = []
    for profile in profiles:
        profile_data = load_profile_from_config(get_profile_file_from_path(profile))
        json_profile = {"profile":profile, "setup":profile_data}
        result.append(json_profile)
    return result
