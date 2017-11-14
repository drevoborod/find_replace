#!/usr/bin/env python3

import sys
import main


try:
    import tkinter
except ImportError:
    can_run_gui = False
else:
    can_run_gui = True


if __name__ == "__main":
    params = main.Config()
    if len(sys.argv) > 1:
        import cli_replace
        params.create_config()
        cli_replace.Commandline(params.parameters)
    else:
        if can_run_gui:
            import gui_replace
            gui_replace.MainGui(params.parse_configfile())
        else:
            message = "Unable to start GUI"
            print(message)
            sys.exit(message)



