#!/usr/bin/env python3

import sys
import argparse
import configparser


DEFAULTS = {
    "config": "config.cfg",
    "postfix": "_result",
    "delimiter": "  #################  ",
    "encoding": "utf-8",
    "number": 0,
    "find": "\n",
    "replace": ", "
}

REQUIRED = ["input", "find", "replace"]


class Config:
    def __init__(self):
        if sys.version_info < (3, 5):
            message = "\nNeed python interpreter version not less than 3.5.\n"\
                        "Your version is {}.".format('.'.join(map(str, sys.version_info[:3])))
            print(message)
            sys.exit(message)
        self.parameters = DEFAULTS.copy()

    def create_config(self):
        """Create configuration dictionary using parameters from defaults, command line and config file."""
        file_opts = self.parse_configfile()
        if file_opts:
            for key in file_opts:
                self.parameters[key] = key
        cmdline_opts = self.parse_cmdline()
        for key in cmdline_opts:
            self.parameters[key] = key

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
        return parser.parse_args()

    def parse_configfile(self):
        """Parse configuration file. Returns False if file cannot be read, else returns its contents."""
        config = configparser.ConfigParser()
        try:
            config.read(self.parameters['config'])
        except (IOError, FileNotFoundError):
            return False
        else:
            return dict(config.items())


class Writeout:
    def __init__(self, filename, postfix, delimiter, encoding):
        if postfix:
            splitted = filename.rsplit(".", maxsplit=1)
            if len(splitted) > 1:
                new_file = splitted[0] + postfix + '.' + splitted[1]
            else:
                new_file = splitted[0] + postfix
        else:
            new_file = filename
        self.file = open(new_file, 'w', encoding=encoding)
        self.delimiter = delimiter

    def write(self, data):
        self.file.write(data + self.delimiter)

    def close(self):
        self.file.close()


def parse_input(infile, search_pattern, replace_pattern, interval, delimiter, postfix, encoding):
    data = open(infile, encoding=encoding)
    to_write = Writeout(infile, postfix, delimiter, encoding)
    result = []
    for string in data:
        res = string.rstrip().split(search_pattern)
        result += res
        if interval:
            while len(result) >= interval:
                to_write.write(replace_pattern.join(result[:interval]))
                result = result[interval:]
        else:
            to_write.write(replace_pattern.join(result))
    to_write.write(replace_pattern.join(result))
    to_write.close()


# Self-test:
if __name__ == "__main__":
    parse_input("text.txt", search_pattern=",", replace_pattern="|")
