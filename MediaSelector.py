"""
Task:
    - Selects the media type to be displayed
    - Make display calls to MediaViewer
    - Make calls to MediaViewer to manipulate the media
    - Display Selection tools
"""
import os
from PyQt6.QtWidgets import QFileDialog


class MediaSelector:
    def __init__(self, base_gui):
        self.base_gui = base_gui
        self.media_files = []
        self.current_index = -1

    def open_folder(self):
        print("Opening Folder...")
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")

        print("Finished picking folder")
        if folder_path:
            self.load_media_files(folder_path)
            self.show_next_file()

    def load_media_files(self, folder_path):
        self.media_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif',
                                          'mp4', 'avi', 'mkv', 'mov')):
                    self.media_files.append(os.path.join(root, file))
        self.current_index = -1

    def show_next_file(self):
        if self.media_files:
            self.current_index = (self.current_index + 1) % len(
                self.media_files)
            self.base_gui.display_media(self.media_files[self.current_index])

    def show_previous_file(self):
        if self.media_files:
            self.current_index = (self.current_index - 1) % len(
                self.media_files)
            self.base_gui.display_media(self.media_files[self.current_index])
