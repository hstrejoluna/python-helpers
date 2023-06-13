import os
import tkinter as tk
from tkinter import filedialog

def select_folder_path():
    root = tk.Tk()
    root.withdraw()

    # Prompt the user to select the folder path using a system dialog
    folder_path = filedialog.askdirectory(title="Select Folder")

    return folder_path

def format_folder_names(folder_path):
    # Get the list of folders inside the input folder
    folders = next(os.walk(folder_path))[1]

    for folder in folders:
        old_name = os.path.join(folder_path, folder)
        new_name = os.path.join(folder_path, folder.replace(" ", "-").lower())

        # Rename the folder
        os.rename(old_name, new_name)

    print("Folder names formatted successfully!")

# Prompt the user to select the folder path
folder_path = select_folder_path()

# Format the folder names
format_folder_names(folder_path)
