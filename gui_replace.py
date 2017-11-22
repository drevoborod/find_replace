#!/usr/bin/env python3

import tkinter as tk
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfile
import main


class MainGui(tk.Tk):
    def __init__(self, params, **kwargs):
        super().__init__(**kwargs)
        self.title("Find and replace")
        tk.Button(text="Input file...", command=self.input_file).grid(row=0, column=0)
        tk.Button(text="Output file...", command=self.output_file).grid(row=0, column=1)


    def input_file(self):
        self.infile = asksaveasfilename()

    def output_file(self):
        self.outfile = askopenfile()


if __name__ == "__main__":
    import sys
    message = "Sorry, this file is not for direct execution. Please use replace.py instead."
    print(message)
    sys.exc_info(message)
