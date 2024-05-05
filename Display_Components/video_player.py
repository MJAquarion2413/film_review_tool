from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaMetaData
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, QSize


class Video_Player(QWidget):
    def __init__(self, signal_warehouse):
        super().__init__()
        self.media_path = r"C:\Users\mjkwe\Downloads\Quick clip magic trick.mp4"
        self.max_size = QSize(854, 480)

        self.signal_warehouse = signal_warehouse
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.media_player.setAudioOutput(self.audio_output)

        # Layout setup
        self.layout = QVBoxLayout()
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        self.button_layout = QHBoxLayout()

        # Media player setup
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.mediaStatusChanged.connect(self.adjust_video_size)

        # Play Button
        self.play_button = QPushButton("Play", self)
        self.play_button.clicked.connect(self.play_media)
        self.button_layout.addWidget(self.play_button)

        # Stop Button
        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_media)
        self.button_layout.addWidget(self.stop_button)

        # Load Button
        self.load_button = QPushButton("Load Media", self)
        self.load_button.clicked.connect(self.set_media_path)
        self.button_layout.addWidget(self.load_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        # Register signals on initialization
        self.signal_warehouse.register_signal('play_video', self.play_button.clicked)
        self.signal_warehouse.register_signal('stop_video', self.stop_button.clicked)
        self.signal_warehouse.register_signal('load_video', self.load_button.clicked)

    def play_media(self):
        if self.media_path:
            self.media_player.play()

    def stop_media(self):
        self.media_player.stop()

    def load_media(self, path):
        self.media_player.setSource(QUrl.fromLocalFile(path))
        self.audio_output.setVolume(50)

    def unload_media(self):
        self.media_player.setSource(QUrl())

    def set_media_path(self):
        #self.media_path = path
        self.load_media(self.media_path)

    def adjust_video_size(self, status):
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            video_resolution = self.media_player.metaData().value(QMediaMetaData.Key.Resolution)
            if video_resolution.isValid():
                adjusted_size = video_resolution.scaled(self.max_size, Qt.AspectRatioMode.KeepAspectRatio)
                self.video_widget.setFixedSize(adjusted_size)
