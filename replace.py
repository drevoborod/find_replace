#!/usr/bin/env python3

import main


try:
    import tkinter
except ImportError:
    can_run_gui = False
else:
    can_run_gui = True


if __name__ == "__main__":
    params = main.Config()
    params.create_config()
    engine = main.Engine(params.parameters)
    if params.params_exist:
        for p in main.REQUIRED:
            if p not in params.parameters:
                main.exit_error("Required parameter is missing: '{}'.".format(p))
        try:
            engine.create_outfile()
            engine.parse_file()
        except main.ParserError as err:
            main.exit_error(err)
        else:
            print("File '{}' successfully created.".format(engine.params["output"]))
    else:
        if can_run_gui:
            import gui_replace
            gui_replace.MainGui(engine)
        else:
            main.exit_error("Unable to start GUI.")
