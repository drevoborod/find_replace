#!/usr/bin/env python3

import sys
import os
import argparse
import configparser


DEFAULTS = {
    "config": "config.cfg",
    "postfix": "_result",
    "delimiter": " ##### ",
    "encoding": "utf-8",
    "number": 0
}

REQUIRED = ["input", "find", "replace"]


class ParserError(Exception): pass


class Config:
    def __init__(self):
        if sys.version_info < (3, 5):
            exit_error("\nNeed python interpreter version not less than 3.5.\n"\
                        "Your version is {}.".format('.'.join(map(str, sys.version_info[:3]))))
        self.parameters = DEFAULTS.copy()
        self.params_exist = False

    def create_config(self):
        """Create configuration dictionary using parameters from defaults, command line and config file."""
        cmdline_opts = self.parse_cmdline()
        for key in cmdline_opts:
            if cmdline_opts[key]:
                self.parameters[key] = cmdline_opts[key]
                if key != "config":
                    self.params_exist = True
        file_opts = self.parse_configfile()
        if file_opts:
            for key in file_opts:
                try:
                    if not cmdline_opts[key]:
                        self.parameters[key] = file_opts[key]
                except KeyError:
                    pass

    def parse_cmdline(self):
        """Parse commandline and return arguments dict."""
        parser = argparse.ArgumentParser()
        parser.add_argument("-c", "--config", help="Configuration file name.")
        parser.add_argument("-i", "--input", help="File to parse.")
        parser.add_argument("-o", "--output", help="Output file.")
        parser.add_argument("-f", "--find", help="Expression to replace.")
        parser.add_argument("-r", "--replace", help="Replacement expression.")
        parser.add_argument("-n", "--number", help="Number of items in one group. Groups are separated by delimiter.")
        parser.add_argument("-d", "--delimiter", help="Word which will be used as delimiter of groups.")
        parser.add_argument("-e", "--encoding", help="Encoding of input and output file.")
        parser.add_argument("-p", "--postfix", help="Optional output file postfix (can be used instead of providing full file name. "
                                                    "In such case, output file name will be input_file_name + postfix).")
        return parser.parse_args().__dict__

    def parse_configfile(self):
        """Parse configuration file. Returns False if file cannot be read, else returns its contents."""
        config = configparser.ConfigParser()
        try:
            configstring = self.add_section_to_config(self.parameters['config'])
        except (IOError, FileNotFoundError):
            return False
        else:
            config.read_string(configstring)
            return dict(config.items(section='DEFAULT'))

    def add_section_to_config(self, filename):
        with open(filename, 'r', encoding=self.parameters["encoding"]) as f:
            config_string = '[DEFAULT]\n' + f.read()
        return config_string


class Engine:
    def __init__(self, params):
        self.params = params

    def create_outfile(self, filename=None):
        """Create file where to write to. Need to be executed firstly!"""
        if not filename:
            if "output" not in self.params:
                splitted = self.params['input'].rsplit(".", maxsplit=1)
                if len(splitted) > 1:
                    filename = splitted[0] + self.params['postfix'] + '.' + splitted[1]
                else:
                    filename = splitted[0] + self.params['postfix']
            else:
                filename = self.params['output']
        try:
            self.outfile = open(filename, 'w', encoding=self.params['encoding'])
        except IOError:
            raise ParserError("Unable to create output file.")
        else:
            self.params['output'] = filename

    def parse_file(self):
        try:
            data = open(self.params["input"], encoding=self.params["encoding"])
        except (IOError, FileNotFoundError):
            raise ParserError("Cannot open file to parse.")
        self.parse(data)

    def escape_replacer(self):
        for item in ["find", "replace", "delimiter"]:
            if "\\r" in self.params[item]:
                self.params[item] = self.params[item].replace("\\r", "\r")
            if "\\n" in self.params[item]:
                self.params[item] = self.params[item].replace("\\n", "\n")
            if "\\t" in self.params[item]:
                self.params[item] = self.params[item].replace("\\t", "\t")

    def parse(self, data):
        """Data can be either file object or string."""
        if not hasattr(self, "outfile"):
            raise ParserError("Output file is not defined.")
        elif self.outfile.closed:
            raise ParserError("Trying to write to already closed output file.")
        if type(data) is str:
            data = [data]
        if self.params["number"]:
            try:
                number = int(self.params["number"])
            except ValueError:
                pass
        self.escape_replacer()
        result = []
        for string in data:
            parsed_string = string.split(self.params["find"])
            if "number" in locals():
                result += parsed_string
                res = result[:]
                while len(res) >= number:
                    self.outfile.write(self.params["replace"].join(res[:number]) + self.params["delimiter"])
                    res = res[number:]
                result = res[:]
            else:
                self.outfile.write(self.params["replace"].join(parsed_string))
        self.outfile.write(self.params["replace"].join(result))
        self.outfile.close()


def exit_error(message):
    print(message)
    sys.exit(message)
