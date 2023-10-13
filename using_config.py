# example file for how you would use a config file

# MUST run using python to correctly use the config file, will not work running with flask

import configparser

from flask import Flask

app = Flask(__name__)


# initialises app configurations
def init(app):
    config = configparser.ConfigParser()
    try:
        print("INIT FUNCTION")
        config_location = "etc/defaults.cfg"
        config.read(config_location)
        
        # gets value for each key from config file, then stores these in app.config object
        app.config['DEBUG'] = config.get("config", "debug")
        app.config['ip_address'] = config.get("config", "ip_address")
        app.config['port'] = config.get("config", "port")
        app.config['url'] = config.get("config", "url")

       
    
    except:
        print("Could not read configs from: ", config_location)



# initialises the app by calling the function above before routes are hit 
init(app)

@app.route('/')
def root():
    return "Hello Napier from the configuration testing app"


@app.route('/config/')
def config():
    s = []
    s.append('debug:' + str(app.config['DEBUG']))
    s.append('port:' + app.config['port'])
    s.append('url:' + app.config['url'])
    s.append('ip_address:' + app.config['ip_address'])
    return ', '.join(s)


if __name__ == '__main__':
    init(app)
    app.run(
        host = app.config['ip_address'],
        port = int(app.config['port'])
    )