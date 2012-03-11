import os
import configparser
import appdirs

from ofxstatement.exceptions import Abort

APP_NAME = 'ofxstatement'
APP_AUTHOR = 'ofx'

def get_default_location():
    cdir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
    return os.path.join(cdir, 'config.ini')

def read(ui, location=None):
    if not location:
        location = get_default_location()

    if not os.path.exists(location):
        raise Abort("Cannot load configuration from %s. " % location)

    config = configparser.SafeConfigParser()
    config.read(location)
    return config

def get_settings(ui, config, section):
    if not config.has_section(section):
        raise Abort("No section named %s in config file" % section)

    import pdb; pdb.set_trace();
    opts = config.get_options(section)
    return zip([(o, config.get(section, o)) for o in opts])
