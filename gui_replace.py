#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askyesno, showerror, showinfo
import main


class MainGui(tk.Tk):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.saved = False      # Indicates if this output file name has been already in use.
        self.title("Find and replace")
        self.search_pattern = tk.StringVar(value=self.engine.params["find"] if "find" in self.engine.params else "")
        self.replace_pattern = tk.StringVar(value=self.engine.params["replace"] if "replace" in self.engine.params else "")
        self.delimiter = tk.StringVar(value=self.engine.params["delimiter"])
        self.blocksize = tk.StringVar(value=self.engine.params["number"])
        self.infile = tk.StringVar(value=self.engine.params["input"] if "input" in self.engine.params else "")
        self.outfile = tk.StringVar(value=self.engine.params["output"] if "output" in self.engine.params else "")
        tk.Button(text="Input file...", command=self.input_file, width=15).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(textvariable=self.infile, width=100).grid(row=0, column=1, padx=5, columnspan=4, sticky="we")
        tk.Button(text="Output file...", command=self.output_file, width=15).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Entry(textvariable=self.outfile, width=100).grid(row=1, column=1, padx=5, columnspan=4, sticky="we")
        tk.Label(text="Search pattern:").grid(row=2, column=0, sticky="e", padx=5)
        tk.Label(text="Replace pattern:").grid(row=2, column=2, sticky="e", padx=5)
        tk.Entry(textvariable=self.search_pattern, width=50).grid(row=2, column=1, padx=5, pady=5, sticky="we")
        tk.Entry(textvariable=self.replace_pattern, width=50).grid(row=2, column=3, padx=5, pady=5, sticky="we")
        tk.Label(text="(\\n, \\t, \\r can be used)").grid(row=3, column=0, columnspan=3, sticky = "ewn")
        tk.Label(text="Separator:").grid(row=4, column=0, sticky="es", pady=5, padx=5)
        tk.Label(text="Block size:").grid(row=4, column=2, sticky="es", pady=5, padx=5)
        tk.Entry(textvariable=self.delimiter, width=50).grid(row=4, column=1, sticky="ws", pady=5, padx=5)
        tk.Entry(textvariable=self.blocksize, width=5).grid(row=4, column=3, sticky="ws", pady=5, padx=5)
        tk.Frame(height=15).grid(row=5, pady=5)
        tk.Button(text="Execute", command=self.execute, width=8).grid(row=6, column=0, sticky="sw", padx=5, pady=5)
        tk.Button(text="Exit", command=self.destroy, width=8).grid(row=6, column=3, sticky="se", padx=5, pady=5)
        self.grid_columnconfigure(0, weight=0, pad=0)
        self.grid_columnconfigure(1, weight=1, pad=0, minsize=100)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1, minsize=100, pad=0)
        for row in list(range(5)) + [6]:
            self.grid_rowconfigure(row, weight=0, minsize=35)
        self.grid_rowconfigure(5, weight=1)
        self.minsize(height=220, width=500)
        self.mainloop()

    def input_file(self):
        res = askopenfilename().strip()
        if res:
            self.infile.set(res)

    def output_file(self):
        res = asksaveasfilename().strip()
        if res:
            self.outfile.set(res)
            self.saved = False

    def set_params(self):
        infile = self.infile.get().strip()
        if infile:
            self.engine.params["input"] = infile
        else:
            showerror("No file to parse", "Please enter file name to parse!")
            return False
        search = self.search_pattern.get()
        if search:
            self.engine.params["find"] = search
        else:
            showerror("Nothing to search", "Please enter search pattern!")
            return False
        replace = self.replace_pattern.get()
        if replace:
            self.engine.params["replace"] = replace
        else:
            showerror("No replace pattern", "Please enter replace expression!")
            return False
        self.engine.params["delimiter"] = self.delimiter.get()
        self.engine.params["number"] = self.blocksize.get()
        outfile = self.outfile.get().strip()
        if outfile:
            self.engine.params["output"] = outfile
        else:
            try:
                self.engine.create_outfile()
            except main.ParserError as err:
                showerror("Unable to create output file", err)
                return False
            else:
                self.outfile.set(self.engine.params["output"])
        return True

    def execute(self):
        if self.set_params():
            if self.saved:
                if askyesno("Export file already used", "Warning! This export file name was already in use.\n"
                                                        "Do you want to select new export file name?"):
                    self.output_file()
                    outfile = self.outfile.get().strip()
                    if outfile:
                        self.engine.params["output"] = outfile
            try:
                self.engine.create_outfile()
                self.engine.parse_file()
            except main.ParserError as err:
                showerror("Unable to open file", err)
            else:
                self.saved = True
                showinfo("File created", "File '{}' successfully created.".format(self.outfile.get()))


if __name__ == "__main__":
    main.exit_error("Sorry, this file is not for direct execution. Please use replace.py instead.")

