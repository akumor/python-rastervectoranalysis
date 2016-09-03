#!/usr/bin/env python

import os
import logging
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
import sys
import getopt
import configparser
import signal
from osgeo import gdal
from osgeo import gdalconst
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt


class RasterVectorAnalysis:
    """
    Class used to produce different representations of Rundeck job schedule data.
    """

    @staticmethod
    def plot_tif(tif_path, cheap_cloud_mask=None):
        """
        Plots the raster created from a TIF file given the path to the TIF.
        :param tif_path: string containing path to the TIF file
        :param cheap_cloud_mask: numpy array used to mask the dataset
        :return:
        """
        dataset = gdal.Open(tif_path, gdalconst.GA_ReadOnly)
        dataset_array = dataset.ReadAsArray()
        if cheap_cloud_mask is not None:
            # Select from the scene where the values are very high and mask them
            dataset_array = ma.masked_array(dataset_array, mask=cheap_cloud_mask)
        plt.imshow(dataset_array, interpolation='nearest', vmin=0, cmap=plt.cm.gist_earth)
        plt.show()

        # Close the dataset
        dataset = None




# Setup logging
LOGGER_NAME = 'disable_rundeck_job'
LOGGER = logging.getLogger(LOGGER_NAME)
LOGGER.setLevel(logging.INFO)
# create console handler with a higher log level
CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
CONSOLE_HANDLER.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
CONSOLE_HANDLER.setFormatter(formatter)
# add the handlers to the logger
LOGGER.addHandler(CONSOLE_HANDLER)


# Dictionary containing cli argument names (keys) and their values
ARG_VALUES = {"server=": "",
              "port=": "",
              "apitoken=": "",
              "credentials=": "",
              "logfilepath=": ""
              }


def signal_handler(signal, frame):
    """
    Handles signals such as SIGINT.
    :param signal: signal number
    :param frame: current stack frame
    """
    # Print Ctrl+C message and exit
    LOGGER.info('You pressed Ctrl+C! Script Exited.')
    sys.exit(0)


def process_args():
    """
    Handles the parsing of command line arguments to the script and modifies global variable ARG_VALUES accordingly.
    """
    global LOGGER
    global CONSOLE_HANDLER
    help_string = '''
Usage:

    rundeck_calendar.py [options]

    -h or
    --help                                   Prints this help menu.

    -s <FQDN or IP> or                       Fully qualified domain name or IP address of the Rundeck server where the
    --server=<FQDN or IP>                    job will be executed.

    -p <port> or
    --port=<port>                            Port to connect to on the Rundeck server in order to access the REST API.

    -a <api token> or                        API token to use to connect to the Rundeck REST API.
    --apitoken=<api token>                   NOTE: Not valid with the --credentials option.

    -c <path to credentials file> or         Path to file containing the credentials used to access the Rundeck REST
    --credentials=<path to credentials>      API. File is a .ini and follows the format:

                                             [credentials]
                                             apitoken=<API token string>

    -L <file path> or
    --logfilepath <file path>                Log script output to specified location.


'''

    # Attempt to use getopt for parsing
    try:
        opt_list, args = getopt.getopt(sys.argv[1:], 'hs:p:a:c:L:', ARG_VALUES.keys())
    except getopt.GetoptError:
        os.system('clear')
        print(help_string)
        sys.exit(2)

    # Assign values from options provided by user to the corresponding option
    # name in the dictionary
    for opt in opt_list:
        if opt[0] in ('-h', '--help') or len(args) > 0:
            print(help_string)
            sys.exit()
        elif opt[0] in ('-s', '--server'):
            ARG_VALUES['server='] = opt[1]
        elif opt[0] in ('-p', '--port'):
            ARG_VALUES['port='] = opt[1]
        elif opt[0] in ('-a', '--apitoken'):
            if ARG_VALUES['apitoken='] != "":
                print("ERROR: --apitoken option is not compatible with --credentials option.")
                print(help_string)
                sys.exit(1)
            ARG_VALUES['apitoken='] = opt[1]
        elif opt[0] in ('-c', '--credentials'):
            if ARG_VALUES['apitoken='] != "":
                print("ERROR: --apitoken option is not compatible with --credentials option.")
                print(help_string)
                sys.exit(1)
            # Do some error checking
            try:
                (head, tail) = os.path.split(opt[1])
                if not os.path.isdir(head):
                    print("ERROR: Invalid path (%s is not a directory) specified for --credentials option." % head)
                    sys.exit(1)
            except Exception as e:
                print(str(e))
                print("ERROR: Invalid path (%s) specified for --credentials option." % opt[1])
                sys.exit(1)
            # Parse the credentials file real quick to get the apitoken
            ARG_VALUES['credentials='] = opt[1]
            config_parser = configparser.ConfigParser()
            config_parser.read(opt[1])
            ARG_VALUES['apitoken='] = config_parser.get("credentials", "apitoken")
        elif opt[0] in ('-u', '--uuid'):
            for uuid in opt[1].split(','):
                ARG_VALUES['uuid='].append(uuid)
        elif opt[0] in ('-C', '--cmdbenvironment'):
            for cmdb_environment in opt[1].split(','):
                ARG_VALUES['cmdbenvironment='].append(cmdb_environment)
        elif opt[0] in ('-L', '--logfilepath'):
            # Do some error checking
            try:
                (head, tail) = os.path.split(opt[1])
                if not os.path.isdir(head):
                    print("ERROR: Invalid path (%s is not a directory) specified for --logfilepath option." % head)
                    sys.exit(1)
            except Exception as e:
                print(str(e))
                print("ERROR: Invalid path (%s) specified for --logfilepath option." % opt[1])
                sys.exit(1)
            ARG_VALUES['logfilepath='] = opt[1]
        elif opt[0] in ('-d', '--disableexecutions'):
            ARG_VALUES['disableexecutions'] = True
        elif opt[0] in ('-D', '--disableschedules'):
            ARG_VALUES['disableschedules'] = True




#################### Main Script ##############################################
if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Process command line arguments
    process_args()

    # Setup file logging
    if not ARG_VALUES["logfilepath="] == "":
        if os.path.isfile(ARG_VALUES["logfilepath="]):
            os.remove(ARG_VALUES["logfilepath="])
        file_hdlr = logging.FileHandler(ARG_VALUES["logfilepath="])
        # add the handler to the logger
        LOGGER.addHandler(file_hdlr)

    RasterVectorAnalysis.plot_tif('/home/akumor/PycharmProjects/python-rastervectoranalysis/tests/test_data/chesapeaketry_1.tif')
