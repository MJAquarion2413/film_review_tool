from PyQt6.QtCore import QSize, Qt, QUrl, QTimer
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, \
    QPushButton, QSpacerItem, QSizePolicy, QHBoxLayout, QStyle
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

from ArrowKeyFilter import ArrowKeyFilter
from ClickableSlider import ClickableSlider
from MediaSelector import MediaSelector


class BaseGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize attributes
        self.h_layout = None
        self.original_pixmap = None
        self.arrow_key_filter = None
        self.position_slider = None
        self.volume_slider = None
        self.title_image_label = None
        self.button_layout = None
        self.media_selector = None
        self.layout = None
        self.open_folder_button = None
        self.next_file_button = None
        self.previous_file_button = None
        self.image_label = None
        self.video_widget = None
        self.slider = None
        self.play_button = None
        self.player = None
        self.audio_output = None
        self.update_timer = None
        self.central_widget = None

        print("# Initializing Base Initialization...")
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.update_timer = QTimer(self)

        # Window Title and Size
        self.setWindowTitle("Miguel's Media Explorer")
        self.setGeometry(0, 0, 500, 350)

        # Initialize UI
        print("# Finished Base Initialization")
        print("& Initializing UI...")
        self.init_ui()

    def init_ui(self):
        print("& Initializing UI...")

        self.arrow_key_filter = ArrowKeyFilter(self)
        self.installEventFilter(self.arrow_key_filter)

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        self.layout = QVBoxLayout(self.central_widget)

        # Title Image
        self.setup_title_image()

        # Video Widget
        self.video_widget = QVideoWidget()
        self.layout.addWidget(self.video_widget)

        # Image Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Player Controls
        self.setup_player_controls()

        print("& Setting Up File Control Buttons...")
        self.setup_file_control_buttons()
        print("& Finished Setting Up File Control Buttons")

        # Setup for the sliders
        self.setup_position_slider()

        # Timer for updating the position slider
        self.update_timer.timeout.connect(self.update_slider_position)
        self.update_timer.start(300)  # Update interval in milliseconds

        # Initial Hide
        self.video_widget.hide()
        self.image_label.hide()

    def setup_title_image(self):
        self.title_image_label = QLabel(self)
        pixmap = QPixmap(
            r'C:\Users\mjkwe\PycharmProjects\film_review_tool\MediaExplorerTitle.png')  # Replace with your image path
        scaled_pixmap_title = pixmap.scaledToWidth(self.width(),
                                                   Qt.TransformationMode.SmoothTransformation)
        self.title_image_label.setPixmap(scaled_pixmap_title)
        self.title_image_label.setFixedHeight(scaled_pixmap_title.height())
        self.title_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_image_label)

    def setup_player_controls(self):
        self.h_layout = QHBoxLayout()

        # Add spacer
        self.h_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                          QSizePolicy.Policy.Minimum))

        # Play Button
        self.play_button = QPushButton()
        pause_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_MediaPause)
        self.play_button.setIcon(pause_icon)
        self.play_button.clicked.connect(self.toggle_playback)
        self.h_layout.addWidget(self.play_button)

        self.setup_volume_slider()

        # Add spacer
        self.h_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                          QSizePolicy.Policy.Minimum))
        self.layout.addLayout(self.h_layout)

    def play_video(self, path):
        # Hide image related widgets and show video related widgets
        self.image_label.hide()
        self.video_widget.show()
        self.play_button.show()
        self.volume_slider.show()
        self.position_slider.show()

        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()

    def show_image(self, path):
        # Hide video related widgets and show image related widgets
        self.video_widget.hide()
        self.play_button.hide()
        self.volume_slider.hide()
        self.position_slider.hide()

        self.original_pixmap = QPixmap(path)
        self.scale_image_to_window(self.original_pixmap)
        self.image_label.show()

    def scale_image_to_window(self, pixmap):
        if pixmap and not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.image_label.width(),
                                          self.image_label.height(),
                                          Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        if self.original_pixmap:
            self.scale_image_to_window(self.original_pixmap)

    def display_media(self, media_path):
        if media_path.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            self.show_image(media_path)
        else:
            self.play_video(media_path)

    def toggle_playback(self):
        if self.player.playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            self.player.play()
            pause_icon = self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPause)
            self.play_button.setIcon(pause_icon)
        else:
            self.player.pause()
            play_icon = self.style().standardIcon(
                QStyle.StandardPixmap.SP_MediaPlay)
            self.play_button.setIcon(play_icon)

    def fast_forward(self):
        current_position = self.player.position()
        self.set_position(current_position + 10000)  # 10 seconds forward

    def rewind(self):
        current_position = self.player.position()
        self.set_position(max(current_position - 10000,
                              0))  # 10 seconds back, not going below 0

    def update_slider_range(self, duration):
        if self.slider is not None:
            self.slider.setRange(0, duration)

    def setup_file_control_buttons(self):
        # Buttons for media control
        self.next_file_button = QPushButton("Next File", self)
        self.previous_file_button = QPushButton("Previous File", self)

        # Layout for buttons
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.next_file_button)
        self.button_layout.addWidget(self.previous_file_button)
        self.layout.addLayout(self.button_layout)

    def setup_media_selector(self):
        print("& Initializing Media Selector...")
        self.media_selector = MediaSelector(self)
        self.next_file_button.clicked.connect(
            self.media_selector.show_next_file)
        self.previous_file_button.clicked.connect(
            self.media_selector.show_previous_file)
        print("& Finished Initializing Media Selector")

        self.setup_menu_bar()


    def set_initial_file(self):
        self.media_selector.open_folder()

    def check_if_objects_exists(self):
        print(f"self.title_image_label: {self.title_image_label}")
        print(f"self.button_layout: {self.button_layout}")
        print(f"self.media_selector: {self.media_selector}")
        print(f"self.layout: {self.layout}")
        print(f"self.next_file_button: {self.next_file_button}")
        print(f"self.previous_file_button: {self.previous_file_button}")
        print(f"self.image_label: {self.image_label}")
        print(f"self.video_widget: {self.video_widget}")
        print(f"self.slider: {self.slider}")
        print(f"self.play_button: {self.play_button}")
        print(f"self.player: {self.player}")
        print(f"self.audio_output: {self.audio_output}")
        print(f"self.update_timer: {self.update_timer}")
        print(f"self.central_widget: {self.central_widget}")

    def setup_volume_slider(self):
        # Volume Slider
        self.volume_slider = ClickableSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)  # Volume range from 0 to 100
        self.volume_slider.setValue(50)  # Set to default volume
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.volume_slider.sliderMoved.connect(self.set_volume_from_slider)

        # Add slider to the layout
        self.h_layout.addWidget(self.volume_slider)

    def setup_position_slider(self):
        # Video Position Slider
        self.position_slider = ClickableSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0,
                                      1000)  # Adjust this range based on video duration
        self.position_slider.sliderMoved.connect(self.set_position)

        # Add sliders to the layout
        self.layout.addWidget(self.position_slider)

    def update_slider_position(self):
        if not self.position_slider.isSliderDown():
            position = self.player.position()
            self.position_slider.setValue(position)

    def set_volume(self, volume):
        self.audio_output.setVolume(volume / 100.0)  # Volume is a percentage

    def set_volume_from_slider(self, position):
        self.volume_slider.setValue(position)
        self.set_volume(position)

    def set_position(self, position):
        self.player.setPosition(position)

    def setup_menu_bar(self):
        # Create the menu bar
        menu_bar = self.menuBar()

        # Create a 'File' menu
        file_menu = menu_bar.addMenu("&File")

        # Create an 'Open' action
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.media_selector.open_folder)  # Connect to the open_folder method

        # Add 'Open' action to 'File' menu
        file_menu.addAction(open_action)
