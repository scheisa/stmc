from configparser import ConfigParser
from os import path, makedirs
import xml.etree.ElementTree as ET

CONFIG_LOCATION = fr"{path.expanduser('~')}/.config/stmc"
CONFIG_FILE = fr"{CONFIG_LOCATION}/config.ini"

def die(status: str, msg: str, exit_code: int):
    color: str = ''

    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'

    match status:
        case "error":
            color = RED
        case "info":
            color = YELLOW
        case "success":
            color = GREEN

    print(f"{color}[{status.upper()}]{RESET}:", end="")
    print(f" {msg}")
    exit(exit_code)

def check_config(config: ConfigParser):
    # create folders if they don't exist
    if not path.exists(CONFIG_LOCATION): 
        makedirs(CONFIG_LOCATION)
    # if config doesn't exist create it and write default values
    if not path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as file:
            config.write(file)

        die("info", f"default config was created at location {CONFIG_FILE} please add url of your miniflux instance and your api key", 0)

def parse_config() -> ConfigParser:
    parser = ConfigParser()

    # default config values
    default_config = {
            "instance": {"url": "", "api": ""},
            "bindings": { "down": "j", "up": "k"},
    }

    for section, options in default_config.items():
        parser[section] = options

    check_config(parser)

    parser.read(CONFIG_FILE)

    return parser
