#!/usr/bin/env python3

import tkinter as tk


class MainGui(tk.Tk):
    def __init__(self, params, **kwargs):
        super().__init__(**kwargs)
        self.params = params



if __name__ == "__main__":
    print("Sorry, this file is not for direct execution. Please use replace.py instead.")
