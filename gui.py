import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from video_manager import

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Video Rating Application")
        self.create_widgets()

    def create_widgets(self):
        # Menu for Directory Selection
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Directory",
                              command=self.select_directory)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

        # Video Display Area (Placeholder)
        self.video_label = tk.Label(self.root, text="Video Display Area",
                                    height=10)
        self.video_label.pack()

        # Control Buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)
        self.next_button = tk.Button(control_frame, text="Next Video",
                                     command=self.next_video)
        self.next_button.pack(side=tk.LEFT)
        self.prev_button = tk.Button(control_frame, text="Last Video",
                                     command=self.last_video)
        self.prev_button.pack(side=tk.LEFT)
        self.rate_button = tk.Button(control_frame, text="Rate Video",
                                     command=self.rate_video)
        self.rate_button.pack(side=tk.LEFT)
        self.delete_button = tk.Button(control_frame, text="Delete Video",
                                       command=self.delete_video)
        self.delete_button.pack(side=tk.LEFT)

        # Rating Interface (Placeholder)
        self.rating_var = tk.IntVar()
        self.rating_dropdown = ttk.Combobox(control_frame,
                                            textvariable=self.rating_var,
                                            values=[i for i in range(1, 11)])
        self.rating_dropdown.pack(side=tk.LEFT)

        # Reaction Textbox
        self.reaction_textbox = tk.Text(self.root, height=5)
        self.reaction_textbox.pack(fill=tk.X)

        # Side Panel for Video Information (Placeholder)
        self.info_label = tk.Label(self.root, text="Video Info Panel")
        self.info_label.pack()

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Ready", bd=1,
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_directory(self):
        # Logic to select directory
        pass

    def next_video(self):
        # Logic for next video
        pass

    def last_video(self):
        # Logic for last video
        pass

    def rate_video(self):
        # Logic to rate video
        pass

    def delete_video(self):
        # Logic to delete video
        pass

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GUI()
    app.run()
