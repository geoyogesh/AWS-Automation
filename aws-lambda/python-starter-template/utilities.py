# -----------------------------------------------------------------------
# utilities.py
#
# common module containing utility functions
#
# -----------------------------------------------------------------------

import logging
import os
import datetime
import sys
from enum import Enum
import configparser


has_error = False


class Environment(Enum):
    prod = 'prod'
    dev = 'dev'

    def __str__(self):
        return self.value


class EmailLog(Enum):
    on_error = 'onerror'
    always = 'always'
    never = 'never'

    def __str__(self):
        return self.value


class LogLevel(Enum):
    critical = 'critical'
    error = 'error'
    warning = 'warning'
    info = 'info'
    debug = 'debug'

    def __str__(self):
        return self.value


# Configure logging for script.
def config_logging(script_name, log_level):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Make logging directory to place if it does not exist already
    temp_dir = os.path.join(os.path.sep, dir_path, 'tmp')
    log_path = os.path.join(temp_dir, 'logs')
    log_dir = os.path.join(os.path.sep, log_path, script_name + '_logs')

    for path in [temp_dir, log_path, log_dir]:
        if not os.path.exists(path):
            os.mkdir(path)

    # Determine logging level from log_level parameter. Ordered by the logging library hierarchy.
    # Chooses NOTSET if input is not found as a level
    if log_level.lower() == 'critical':
        log_level = logging.CRITICAL
    elif log_level.lower() == 'error':
        log_level = logging.CRITICAL
    elif log_level.lower() == 'warning':
        log_level = logging.WARNING
    elif log_level.lower() == 'info':
        log_level = logging.INFO
    elif log_level.lower() == 'debug':
        log_level = logging.DEBUG
    else:
        log_level = logging.NOTSET

    logging.basicConfig(filename=log_dir + '/' + datetime.datetime.now().strftime("%Y-%m-%d") + '.log',
                        format='[%(asctime)s]' + '[%(levelname)s]: %(message)s', datefmt="%H:%M:%S %p",
                        level=log_level)

    log_info('------------------------------------------------------')


# Write with log level INFO to log file
def log_info(msg):
    exc_info = sys.exc_info()
    if exc_info[0] is not None:  # If there is currently no exception, exc_info is (None, None, None)
        logging.info(msg, exc_info=exc_info)
        print_log('{0}: {1}'.format(exc_info[0], exc_info[1]))
    else:
        logging.info(msg)
    print_log('INFO: ' + msg)


# Write with log level ERROR to log file.
def log_error(msg):
    global has_error
    has_error = True
    exc_info = sys.exc_info()
    if exc_info[0] is not None:  # If there is currently no exception, exc_info is (None, None, None)
        logging.error(msg, exc_info=exc_info)
        print_log('{0}: {1}'.format(exc_info[0], exc_info[1]))
    else:
        logging.error(msg)
    print_log('ERROR: ' + msg)


# Write with log level WARNING to log file
def log_warning(msg):
    exc_info = sys.exc_info()
    if exc_info[0] is not None:  # If there is currently no exception, exc_info is (None, None, None)
        logging.warning(msg, exc_info=exc_info)
        print_log('{0}: {1}'.format(exc_info[0], exc_info[1]))
    else:
        logging.warning(msg)
    print_log('WARNING: ' + msg)


# Write with log level EXCEPTION to log file. Should only be called in exception handler.
def log_exception(msg):
    global has_error
    has_error = True
    # Get exception info
    exc_info = sys.exc_info()
    # If called with no exception to handle, log message without the exception with log level ERROR
    if exc_info is None:
        log_error(msg)
    # If exception is a Warning, log message with log level WARNING
    elif exc_info is Warning:
        log_warning(msg)
    # Else, the exception is logged with the exception with log level ERROR
    else:
        logging.exception(msg, exc_info=exc_info)
        print_log('{0}: {1}'.format(exc_info[0], exc_info[1]))
        print_log('ERROR: ' + msg)


# Prints the log message to console
def print_log(msg):
    print(msg)


# Call this in last log to the log file for line breaks at the end of the run. Writes to log file with level info
def log_end_run(msg):
        log_info(msg)
        log_info('------------------------------------------------------\n\n')


def read_parameters():
    # utilities.list_files_folders()
    print('Log Level: {0}'.format(os.environ['log_level']))
    print('Environment: {0}'.format(os.environ['script_environment']))
    return {
        'script_environment': Environment[os.environ['script_environment']] if 'script_environment' in os.environ and os.environ['script_environment'] else Environment.dev,  # script_environment dev (default), prod
        'email_log': EmailLog[os.environ['email_log']] if 'email_log' in os.environ and os.environ['email_log'] else EmailLog.never,  # onerror, always, never (default)
        'log_level': LogLevel[os.environ['log_level']] if 'log_level' in os.environ and os.environ['log_level'] else LogLevel.info  # critical, error, debug, info (default)
    }


# Read configuration file and returns the parameters python dictionary
def read_config_file(config_section, config_file):
    variables = {}
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.RawConfigParser()
    file_path = os.path.join(os.path.sep, dir_path, 'config', config_file + '.cfg')
    if config.read(file_path) == []:
        log_error('Could not read from config file {}'.format(file_path))
        return {}
    if not config.has_section(str(config_section)):
        log_error('Could not find configuration section {0} in file {1}'.format(str(config_section), file_path))
        return {}
    try:
        if config_file == 'python-starter-script':
            opts = ['param1', 'param2', 'param3']
            # The option names will be used as dictionary keys with which to retrieve variable values
            for key in opts:
                variables[key] = config.get(str(config_section), key)
    except configparser.NoOptionError:
        log_exception('Missing a variable in section {0} in file {1}'.format(str(config_section), file_path))
    return variables


# debug functions
def list_files_folders():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print ('current directory: ' + dir_path)
    for path, subdirs, files in os.walk(dir_path):
        for name in files:
            print (os.path.join(path, name))

