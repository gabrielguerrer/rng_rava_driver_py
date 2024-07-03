"""
Copyright (c) 2023 Gabriel Guerrer

Distributed under the MIT license - See LICENSE for details
"""

"""
Configuration functionality for RAVA_APP using configparser's module.
"""

import os
import logging
import configparser


### RAVA_CFG

class RAVA_CFG:

    def __init__(self, cfg_filename, cfg_str):
        self.name = 'RAVA_CFG'
        self.lg = logging.getLogger('rava')        

        # Initialize parser
        self.cfg_filename = cfg_filename
        self.cfg_parser = self.parser_init(cfg_filename, cfg_str)


    # Low level functionality

    def parser_init(self, cfg_filename, cfg_str):
        # Default cfg
        cfg_default = configparser.ConfigParser()
        cfg_default.read_string(cfg_str)

        # Config file already exists?
        if os.path.isfile(cfg_filename):

            # Read cfg info
            cfg_parser = configparser.ConfigParser()
            cfg_parser.read(cfg_filename)

            # The read cfg contains all the expected entries?
            for key in cfg_default:
                if key not in cfg_parser or set(cfg_parser[key].keys()) != set(cfg_default[key].keys()):
                    os.remove(cfg_filename)
                    self.lg.error('{} Config: The provided config file is incomplete. Please restart the application.'.format(self.name))
                    exit()

        # Config file inexists, create it with default values
        else:
            self.lg.info('{} Config: Creating file with default content'.format(self.name))
            cfg_parser = cfg_default
            
            # Save
            with open(cfg_filename, 'w') as cfg_file:
                cfg_parser.write(cfg_file)

        return cfg_parser


    # High level functionality

    def read(self, section, option, type=str):
        # Return config option in the appropriate type
        if type is int:
            data = self.cfg_parser.getint(section, option)
        elif type is float:
            data = self.cfg_parser.getfloat(section, option)
        elif type is bool:
            data = self.cfg_parser.getboolean(section, option)
        else:
            data = self.cfg_parser.get(section, option)

        return data


    def write(self, section, option, value, save=True):
        # Write config option
        if type(value) is not str:
            value = str(value)
        self.cfg_parser.set(section, option, value)
        
        # Save?
        if save:
            with open(self.cfg_filename, 'w') as cfg_file:
                self.cfg_parser.write(cfg_file)