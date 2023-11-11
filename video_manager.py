import os


class VideoManager:
    def __init__(self, gui):
        self.gui = gui
        self.video_files = []
        self.current_index = -1

    def load_videos_from_directory(self, directory):
        # Load all video files from the specified directory
        self.video_files = [os.path.join(directory, f) for f in
                            os.listdir(directory) if
                            f.endswith(('.mp4', '.m4v'))]
        self.current_index = 0 if self.video_files else -1
        self.update_video_display()

    def next_video(self):
        # Move to the next video in the list
        if self.video_files and self.current_index < len(self.video_files) - 1:
            self.current_index += 1
            self.update_video_display()

    def previous_video(self):
        # Move to the previous video in the list
        if self.video_files and self.current_index > 0:
            self.current_index -= 1
            self.update_video_display()

    def update_video_display(self):
        # Update the GUI with the current video
        if 0 <= self.current_index < len(self.video_files):
            current_video = self.video_files[self.current_index]
            # Here you would typically call a method in the GUI to update the
            # video display For example: self.gui.update_video_player(
            # current_video)
            print(
                f"Current video: {current_video}")  # Placeholder for actual video update logic

    def get_current_video(self):
        # Return the current video file path
        if 0 <= self.current_index < len(self.video_files):
            return self.video_files[self.current_index]
        return None
