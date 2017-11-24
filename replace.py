#!/usr/bin/env python3

import sys
import main


try:
    import tkinter
except ImportError:
    can_run_gui = False
else:
    can_run_gui = True


if __name__ == "__main__":
    params = main.Config()
    if len(sys.argv) > 1:
        params.create_config()
        for p in main.REQUIRED:
            if p not in params.parameters:
                main.exit_error("Required parameter is missing: '{}'.".format(p))
        engine = main.Engine(params.parameters)
        engine.create_outfile()
        engine.parse()
        engine.close()
    else:
        if can_run_gui:
            import gui_replace
            params.create_config()
            engine = main.Engine(params.parameters)
            gui_replace.MainGui(engine)
        else:
            main.exit_error("Unable to start GUI.")



