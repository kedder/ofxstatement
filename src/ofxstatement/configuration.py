from typing import Optional
from collections.abc import MutableMapping
import os
import configparser
import appdirs

from ofxstatement.exceptions import Abort

APP_NAME = "ofxstatement"
APP_AUTHOR = "ofx"


def get_default_location() -> str:
    cdir = appdirs.user_config_dir(APP_NAME, APP_AUTHOR)
    return os.path.join(cdir, "config.ini")


def read(location: str = None) -> Optional[MutableMapping]:
    if not location:
        location = get_default_location()

    if not os.path.exists(location):
        return None

    config = configparser.ConfigParser()
    config.read(location)
    return config


def get_settings(config, section: str):
    if not config.has_section(section):
        raise Abort("No section named %s in config file" % section)

    opts = config.get_options(section)
    return zip([(o, config.get(section, o)) for o in opts])
