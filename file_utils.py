################################################
#
# Handles alerts folder selection,
# Eventually handle button population(?)
#
################################################

import json
import tkinter as tk
from tkinter import filedialog

#class FileManager(object):
#    def __init__(self, alert_dir="~/Music"):
#        self.alert_dir = alert_dir

def open_dir_dialogue(init_dir):
    root = tk.Tk()
    root.withdraw() # Hide Tkinter main screen (only want dialogue to be open)

    # TODO: Currently if the dialogue disappears (user clicks off of it)
    # before the folder is selected, it freezes the entire program.
    # Must find a solution to fix that.
    root.wm_attributes("-topmost", 1)

    dir_path = filedialog.askdirectory(
        initialdir=init_dir,
        title="Select Alerts Directory",
        mustexist=True
    )
    return dir_path

# Update settings.json file
def update_settings(settings, settings_path):
    with open(settings_path, "w") as f:
        json.dump(settings, f)

# Load settings.json arguments
# Returns a dict
def load_settings(settings_path):
    with open(settings_path, "r") as f:
        return json.load(f)