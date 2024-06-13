import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog
from Helpers.config import get_settings ,Settings
class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Sorter")
        
        self.label = tk.Label(root, text="Select a folder to sort files")
        self.label.pack(pady=10)
        
        self.select_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)
        
        self.undo_button = tk.Button(root, text="Undo", command=self.undo_changes)
        self.undo_button.pack(pady=10)

        self.folder_path = tk.StringVar()
        self.folder_label = tk.Label(root, textvariable=self.folder_path)
        self.folder_label.pack(pady=10)
        
        self.log_file = "file_sorter_log.json"
        self.file_log = {}
        self.folders_created = []

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.sort_files(folder_selected)

    def sort_files(self, folder_path):
        
        app_settings = get_settings()
        file_types = {
            'File-Flick-Images': app_settings.IMAGES,
            'File-Flick-Videos': app_settings.VIDEOS,
            'File-Flick-Documents': app_settings.DOCUMENTS
        }
        
        # Create folders for each file type and an "Others" folder
        for file_type in file_types.keys():
            folder = os.path.join(folder_path, file_type)
            if not os.path.exists(folder):
                os.makedirs(folder)
                self.folders_created.append(folder)
                
        others_folder = os.path.join(folder_path, 'Others')
        if not os.path.exists(others_folder):
            os.makedirs(others_folder)
            self.folders_created.append(others_folder)

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                moved = False
                for file_type, extensions in file_types.items():
                    if any(filename.lower().endswith(ext) for ext in extensions):
                        new_path = os.path.join(folder_path, file_type, filename)
                        shutil.move(file_path, new_path)
                        self.file_log[file_path] = new_path
                        moved = True
                        break
                if not moved:
                    new_path = os.path.join(others_folder, filename)
                    shutil.move(file_path, new_path)
                    self.file_log[file_path] = new_path

        self.save_log()

    def save_log(self):
        log_data = {
            'file_log': self.file_log,
            'folders_created': self.folders_created
        }
        with open(self.log_file, 'w') as f:
            json.dump(log_data, f)

    def load_log(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                log_data = json.load(f)
                self.file_log = log_data.get('file_log', {})
                self.folders_created = log_data.get('folders_created', [])
        else:
            self.file_log = {}
            self.folders_created = []

    def undo_changes(self):
        self.load_log()
        for original_path, new_path in self.file_log.items():
            if os.path.exists(new_path):
                shutil.move(new_path, original_path)
        
        # Remove created folders if they are empty
        for folder in self.folders_created:
            if os.path.exists(folder) and not os.listdir(folder):
                os.rmdir(folder)
        
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        self.file_log = {}
        self.folders_created = {}

