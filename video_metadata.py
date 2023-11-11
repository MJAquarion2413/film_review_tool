from moviepy.editor import VideoFileClip


class VideoMetadata:
    def __init__(self, video_path):
        self.video_path = video_path

    def get_metadata(self):
        # Extract metadata from the video
        with VideoFileClip(self.video_path) as clip:
            duration = clip.duration
            size = os.path.getsize(self.video_path)
            return {
                "duration": duration,
                "size": size
            }
