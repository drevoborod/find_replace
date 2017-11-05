#!/usr/bin/env python3

POSTFIX = "_result"
DELIMITER = "  #################  "
ENCODING = 'utf-8'


class FileError(Exception): pass
class ParseError(Exception): pass


class Writeout:
    def __init__(self, filename):
        splitted = filename.rsplit(".", maxsplit=1)
        if len(splitted) > 1:
            new_file = splitted[0] + POSTFIX + '.' + splitted[1]
        else:
            new_file = splitted[0] + POSTFIX
        self.file = open(new_file, 'w', encoding=ENCODING)

    def write(self, data, delim=None):
        self.file.write(data + delim if delim else DELIMITER)

    def close(self):
        self.file.close()


def parse_input(infile, search_pattern, replace_pattern, interval=0):
    data = open(infile, encoding=ENCODING)
    to_write = Writeout(infile)
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
