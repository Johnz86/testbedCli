"""
Created on 10.12.2013
@author: Jan Jakubcik
@description: Includes all functions, that manipulate and parse json files
"""

import os.path
import json
import logging

def load_json_from_file(file_path):
    """Load the json data from file at file path."""
    if os.path.isfile(file_path):
        logging.debug("Loading json data from file:"+file_path)
        file_data = open(file_path)
        data = json.load(file_data, object_hook=decode_dict)
        return data
    else:
        logging.error("File path {0} is not a file:".format(file_path))

def decode_list(data):
    """Decode json list data."""
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv

def decode_dict(data):
    """Decode json dictionary data."""
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv