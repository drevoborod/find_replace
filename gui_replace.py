#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfile
import main


class MainGui(tk.Tk):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.title("Find and replace")
        self.search_pattern = tk.StringVar(value=self.engine.params["find"] if "find" in self.engine.params else "")
        self.replace_pattern = tk.StringVar(value=self.engine.params["replace"] if "replace" in self.engine.params else "")
        self.delimiter = tk.StringVar(self.engine.params["delimiter"])
        self.blocksize = tk.IntVar(self.engine.params["number"])
        tk.Button(text="Input file...", command=self.input_file).grid(row=0, column=0)
        tk.Button(text="Output file...", command=self.output_file).grid(row=0, column=1)
        # ToDo: Show input and output file names.

        tk.Label(text="Find pattern:").grid(row=1, column=0)
        tk.Label(text="Replace pattern:").grid(row=1, column=1)
        tk.Entry(textvariable=self.search_pattern).grid(row=2, column=0)
        tk.Entry(textvariable=self.replace_pattern).grid(row=2, column=1)
        tk.Label(text="\\n, \\t, \\r can be used").grid(row=3, column=0, columnspan=2)
        tk.Label(text="Separator:").grid(row=4, column=0, anchor="n", pady=5)
        tk.Label(text="Block size:").grid(row=4, column=1, anchor="n", pady=5)
        tk.Entry(textvariable=self.delimiter, width=10).grid(row=5, column=0)
        tk.Entry(textvariable=self.blocksize, width=5).grid(row=5, column=1)
        tk.Frame(height=15).grid(row=6, pady=5)
        tk.Button(text="Execute", command=self.execute).grid(row=7, column=0, sticky="sw")
        tk.Button(text="Exit", command=self.destroy).grid(row=7, column=1, sticky="se")
        self.mainloop()

    def input_file(self):
        self.infile = asksaveasfilename()

    def output_file(self):
        self.outfile = askopenfile()

    def execute(self):
        pass


if __name__ == "__main__":
    import sys
    message = "Sorry, this file is not for direct execution. Please use replace.py instead."
    print(message)
    sys.exc_info(message)
