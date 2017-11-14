#!/usr/bin/env python3

import sys


import cli_replace
import gui_replace
import main

try:
    import tkinter
except ImportError:
    can_run_gui = False
else:
    can_run_gui = True






if __name__ == "__main":
    if len(sys.argv) > 1:
        params = main.Config()
        cli_replace.Commandline(params.parameters)



