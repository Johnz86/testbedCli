import os
import pickle
import ConfigParser
import collections

def get_profile_file_from_path(profile_path, file_format = ".txt"):
    return os.path.join(profile_path, os.path.basename(profile_path)+file_format)

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
        print "Failed to load profiles. Cache profile {0} file dose not exist.".format(profile_pickle_file)
        exit(1)


def get_all_profiles(profile_pickle_file):
    profiles = load_profile_list(profile_pickle_file)
    result = []
    for profile in profiles:
        profile_data = load_profile_from_config(get_profile_file_from_path(profile))
        json_profile = {"profile":profile, "setup":profile_data}
        result.append(json_profile)
    return result
