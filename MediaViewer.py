from PyQt6.QtCore import QEvent, QObject, QTimer, QUrl, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, \
    QStyle
from PyQt6.QtWidgets import QMainWindow, QPushButton, QSlider, QVBoxLayout, \
    QWidget


class MediaViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio = None
        self.volume_slider = None
        self.update_timer = None
        self.slider = None
        self.stop_button = None
        self.play_button = None
        self.player = None
        self.image_label = None
        self.video_widget = None
        self.layout = None
        self.central_widget = None
        self.arrow_key_handler = None

        self.setWindowTitle("Miguel's Media Explorer")

        # Window size
        self.setGeometry(700, 200, 800, 600)

        # Initialize window UI
        self.init_ui()

    def init_ui(self):

        # Set Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set Layout, vertical box layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Sets up the image for the title
        title_image_label = QLabel(self)
        pixmap = QPixmap(
            r'C:\Users\mjkwe\PycharmProjects\film_review_tool\MediaExplorerTitle.png')  # Replace with your image path
        scaled_pixmap = pixmap.scaledToWidth(self.width(),
                                             Qt.TransformationMode.SmoothTransformation)  # Scale the image to the width of the window
        scaled_pixmap = scaled_pixmap.scaledToHeight(self.height() // 10,
                                                     Qt.TransformationMode.SmoothTransformation)  # Scale the image to the height of the window
        title_image_label.setPixmap(scaled_pixmap)
        title_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_image_label.setFixedSize(self.width(), scaled_pixmap.height())
        self.layout.addWidget(title_image_label)

        # Video Widget
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Image Label
        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        # Media Player
        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)

        h_layout = QHBoxLayout()

        # Add a spacer to the left
        h_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum))

        # Player Controls
        """
        Play -> toggle_video_playback
        Stop -> stop_video
        Move_Silder -> set_position
        """
        self.play_button = QPushButton()

        pause_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPause)
        self.play_button.setIcon(pause_icon)
        self.play_button.setSizePolicy(QSizePolicy.Policy.Fixed,
                                       QSizePolicy.Policy.Fixed)

        self.play_button.clicked.connect(self.set_playing_state)

        h_layout.addWidget(self.play_button)

        # Add a spacer to the right
        h_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                     QSizePolicy.Policy.Minimum))

        # Add the horizontal layout to the main layout
        self.layout.addLayout(h_layout)

        self.slider = ClickableSlider(parent=Qt.Orientation.Horizontal,
                                      media_viewer=self)
        self.slider.sliderMoved.connect(self.set_position)
        self.layout.addWidget(self.slider)

        self.player.positionChanged.connect(self.update_slider_position)
        self.player.durationChanged.connect(self.update_slider_range)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_position)
        self.update_timer.start(300)  # Update every 100 milliseconds

        # Volume Slider
        # self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        # self.volume_slider.setRange(0, 100)  # Volume range from 0 to 100
        # self.volume_slider.setValue(self.player.set)  # Set to current volume
        # self.volume_slider.valueChanged.connect(self.player.setVolume)

        # Add the volume slider to the layout
        # Ensure this is placed next to the play button
        self.layout.addWidget(self.volume_slider)

        # Initial Hide
        self.video_widget.hide()
        self.image_label.hide()

    def update_position(self):
        position = self.player.position()
        self.slider.setValue(position)

    def play_video(self, path):
        self.image_label.hide()
        self.video_widget.show()
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()

    def show_image(self, path):
        self.video_widget.hide()
        pixmap = QPixmap(path)
        self.image_label.setPixmap(pixmap)
        self.image_label.show()

    def set_playing_state(self):
        if self.player.playbackState() != \
                QMediaPlayer.PlaybackState.PlayingState:
            self.player.play()
            self.player.play()
            pause_icon = self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPause)
            self.play_button.setIcon(pause_icon)
        else:
            self.player.pause()
            play_icon = self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay)
            self.play_button.setIcon(play_icon)

    def set_position(self, position):
        self.player.setPosition(position)

    def update_slider_position(self, position):
        self.slider.blockSignals(True)  # Prevent the sliderMoved signal
        self.slider.setValue(position)
        self.slider.blockSignals(False)

    def update_slider_range(self, duration):
        self.slider.setRange(0, duration)

    def keyPressEvent(self, event):
        print(f"key pressed: {event.key()}")
        print(f"{self}")
        if event.key() == Qt.Key.Key_Right:
            print("right key pressed")
            self.fast_forward()
        elif event.key() == Qt.Key.Key_Left:
            print("left key pressed")
            self.rewind()
        super().keyPressEvent(event)

    def setPlayerMediaSource(self, path):
        self.player.setSource(QUrl.fromLocalFile(path))

    def fast_forward(self):
        current_position = self.player.position()
        self.set_position(current_position + 10000)  # 10 seconds forward

    def rewind(self):
        current_position = self.player.position()
        self.set_position(max(current_position - 10000,
                              0))  # 10 seconds back, not going below 0


class ClickableSlider(QSlider):
    def __init__(self, parent=None, media_viewer=None):
        super().__init__(parent)
        self.media_viewer = media_viewer

    def mousePressEvent(self, event):
        # Calculate the slider value based on mouse position
        if event.button() == Qt.MouseButton.LeftButton:
            value = self.minimum() + ((
                                                  self.maximum() - self.minimum()) * event.position().x()) / self.width()

            self.blockSignals(True)
            ###
            self.setValue(int(value))
            self.media_viewer.set_position(int(value))
            ###
            self.blockSignals(False)
            event.accept()
        else:
            super().mousePressEvent(event)
