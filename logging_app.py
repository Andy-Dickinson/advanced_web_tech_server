# each time an apps page is visited, a new log file should be added to var/loggingapp.log
# (on linux) can tail the log so each new log line added can be seen in real time, enter in console window:
# tail -f var/loggingapp.log
# -f option follows the log, so each new line is displayed in terminal
# (on windows - powershell):
# Get-Content -Path "C:\path\to\your\log\file.log" -Wait

import configparser
import logging

from logging.handlers import RotatingFileHandler
from flask import Flask, url_for

# flask app is created
app = Flask(__name__)


@app.route('/')
def root():
    this_route = url_for('.root')

    # logs a test message to file, info could be replaced with another level such as debug, error, warn etc
    # see log file to see the effect
    # log whatever you think is important for debugging - too much takes up space, too little may not help fix issues
    app.logger.info("Logging a test message from " + this_route)
    return "Hello Napier from the configurattion testing app (Now with added logging)"


# initialises app configurations, also configures event logging
# see Python logging documentation if wanting to make changes
# as setup here, produces files that cope well with lots of data, easy to read and which can be automatically processed
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = "etc/logging.cfg"
        config.read(config_location)

        # gets value for each key from config file, then stores these in app.config object  
        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

        app.config['log_file'] = config.get("logging", "name")
        app.config['log_location'] = config.get("logging", "location")
        app.config['log_level'] = config.get("logging", "level")
    except:
        print("Could not read configs from: ", config_location)


# to use the logger we initialise the logging system by calling the configuration modules logs() function
# from then we can log messages using the app.logger.warn() and passing in a string - there are also other logging levels (e.g. debug  or error) that we can distinguish the importance of different messages in the logs. See Python logging documentation
def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    # Creates a RotatingFileHandler to manage log files. It rotates log files when they reach a certain size (maxBytes) and keeps a maximum number of backup log files (backupCount).
    file_handler = RotatingFileHandler(log_pathname, maxBytes=1024 * 1024 * 10, backupCount=1024)
    # sets the log level for the handler based on configuration 'log_level'
    file_handler.setLevel(app.config['log_level'])
    # defines log message format: level | timestamp | module name | function name | message
    formatter = logging.Formatter("%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s")
    # sets format
    file_handler.setFormatter(formatter)
    # sets log level for the flask application logger
    app.logger.setLevel( app.config['log_level'] )
    # adds file handler to the flask applications logger
    app.logger.addHandler(file_handler)


# function calls
init(app)
logs(app)


if __name__ == '__main__':
    init(app)
    logs(app)
    app.run(
        host=app.config['ip_address'],
        port=int(app.config['port'])
    )