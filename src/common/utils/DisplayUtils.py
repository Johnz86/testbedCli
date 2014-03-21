"""
Created on 12.10.2013
@author: Jan Jakubcik
@description: Basic Display functions for command line interface.
"""
import logging
from libs.prettytable import PrettyTable

def print_key_value_pair(data):
    """Print basic key value data in form of delimited pair"""
    for item in data:
        logging.info(" %-25s :'%s'" % ("["+str(item)+"]", data[item]))

def print_table_list(header, data):
    """Print list value data in form of table"""
    table = PrettyTable()
    table.add_column(header,data)
    table.align = "l"
    logging.info(table)

def print_table_key_value(data):
    """Print basic key value data in form of table"""
    table = PrettyTable(["Key","Value"])
    table.align = "l"
    for item in data:
        table.add_row([item,data[item]])
    logging.info(table)

def print_list_enum(data_list):
    """Print list data with enumerated index"""
    for index, values in enumerate(data_list):
        print " [{0}]:\t{1}".format(index,values)