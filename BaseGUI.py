from PyQt6.QtCore import QSize, Qt, QUrl, QTimer
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtWidgets import QLineEdit, QListWidget, QMainWindow, QSpinBox, \
    QWidget, \
    QVBoxLayout, \
    QLabel, \
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
        self.inner_vbox = None
        self.rating_input = None
        self.tag_input = None
        self.h_box_inner_vbox_right = None
        self.h_box_inner_vbox_left = None
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
        self.play_button = None
        self.player = None
        self.audio_output = None
        self.update_timer = None
        self.central_widget = None

        print("# Initializing Base Initialization...")
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        # Window Title and Size
        self.setWindowTitle("Miguel's Media Explorer")
        self.setGeometry(0, 0, 963, 600)

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

        self.inner_hbox = QHBoxLayout()

        # Video Widget
        self.video_widget = QVideoWidget()
        self.video_widget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.video_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                        QSizePolicy.Policy.Expanding)
        self.inner_hbox.addWidget(self.video_widget)

        self.setup_rating_tag_widget()

        self.layout.addLayout(self.inner_hbox)

        # Image Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.player.durationChanged.connect(self.update_slider_range)

        # Player Controls
        self.setup_player_controls()

        print("& Setting Up File Control Buttons...")
        self.setup_file_control_buttons()
        print("& Finished Setting Up File Control Buttons")

        # Setup for the sliders
        self.setup_position_slider()

        # Initial Hide
        self.video_widget.hide()
        self.image_label.hide()

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
        self.play_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.h_layout.addWidget(self.play_button)

        # Add spacer
        self.h_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding,
                                          QSizePolicy.Policy.Minimum))

        self.layout.addLayout(self.h_layout)

    def play_video(self, path):
        # Hide image related widgets and show video related widgets
        self.image_label.hide()
        self.video_widget.show()
        self.play_button.show()
        self.position_slider.show()

        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()
        self.set_volume(0.5)

    def show_image(self, path):
        # Hide video related widgets and show image related widgets
        self.video_widget.hide()
        self.play_button.hide()
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

    def update_slider_range(self, duration):
        self.position_slider.setRange(0, duration)

    def setup_file_control_buttons(self):
        # Buttons for media control
        self.next_file_button = QPushButton("Next File", self)
        self.next_file_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.previous_file_button = QPushButton("Previous File", self)
        self.previous_file_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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

    def setup_position_slider(self):
        # Video Position Slider
        self.position_slider = ClickableSlider(Qt.Orientation.Horizontal, self)

        self.position_slider.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.position_slider.valueChanged.connect(self.update_slider_position)

        # Add sliders to the layout
        self.layout.addWidget(self.position_slider)

    def update_slider_position(self, position):
        self.position_slider.blockSignals(True)
        self.player.setPosition(position)
        self.position_slider.blockSignals(False)

    def set_volume(self, volume):
        self.audio_output.setVolume(volume)  # Volume is a percentage

    def setup_menu_bar(self):
        # Create the menu bar
        menu_bar = self.menuBar()

        # Create a 'File' menu
        file_menu = menu_bar.addMenu("&File")

        # Create an 'Open' action with text for shortcut being 'Shift+O'
        open_action = QAction("&Open", self)
        open_action.setShortcut("Shift+O")
        open_action.setShortcutContext(Qt.ShortcutContext.ApplicationShortcut)
        open_action.setToolTip("Open a folder of media files")
        open_action.setStatusTip("Open a folder of media files")
        open_action.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_DialogOpenButton))
        open_action.triggered.connect(
            self.media_selector.open_folder)  # Connect to the open_folder method

        # Create a 'Next File' action with text for chortcut being 'Spacebar'
        next_file_action = QAction("&Next File", self)
        next_file_action.setShortcut("Space")
        next_file_action.setShortcutContext(
            Qt.ShortcutContext.ApplicationShortcut)
        next_file_action.setToolTip("Open the next file in the folder")
        next_file_action.setStatusTip("Open the next file in the folder")
        next_file_action.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowForward))
        next_file_action.triggered.connect(
            self.media_selector.show_next_file)

        # Create a 'Previous File' action with text for chortcut being 'Shift + Spacebar'
        previous_file_action = QAction("&Previous File", self)
        previous_file_action.setShortcut("Shift+Space")
        previous_file_action.setShortcutContext(
            Qt.ShortcutContext.ApplicationShortcut)
        previous_file_action.setToolTip("Open the previous file in the folder")
        previous_file_action.setStatusTip(
            "Open the previous file in the folder")
        previous_file_action.setIcon(self.style().standardIcon(
            QStyle.StandardPixmap.SP_ArrowBack))
        previous_file_action.triggered.connect(
            self.media_selector.show_previous_file)

        # Add Qactions to the 'File' menu
        file_menu.addAction(open_action)
        file_menu.addAction(next_file_action)

    def setup_title_image(self):
        self.title_image_label = QLabel(self)
        pixmap = QPixmap(
            r'C:\Users\mjkwe\PycharmProjects\film_review_tool\MediaExplorerTitle.png')  # Replace with your image path
        scaled_pixmap_title = pixmap.scaledToWidth(self.width(),
                                                   Qt.TransformationMode.SmoothTransformation)
        # crop the pixmap from below
        scaled_pixmap_title = scaled_pixmap_title.copy(0, 0,
                                                       scaled_pixmap_title.width(),
                                                       scaled_pixmap_title.height() - 80)
        self.title_image_label.setPixmap(scaled_pixmap_title)
        self.title_image_label.setFixedHeight(scaled_pixmap_title.height())
        self.title_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_image_label)

    def set_initial_file(self, folder_path):
        if folder_path:
            self.media_selector.load_media_files(folder_path)
            self.media_selector.show_next_file()

    def setup_rating_tag_widget(self):
        self.inner_vbox = QVBoxLayout()
        # rating Spinbox
        self.rating_input = QSpinBox(self)
        self.rating_input.setRange(0, 10)
        self.rating_input.setSingleStep(1)
        self.rating_input.setValue(0)
        self.rating_input.setFixedWidth(100)
        self.rating_input.setFixedHeight(25)
        # keep the rating spinbox from expanding in width
        size_policy = QSizePolicy(QSizePolicy.Policy.Fixed,
                                  QSizePolicy.Policy.Fixed)
        self.rating_input.setSizePolicy(size_policy)
        self.inner_vbox.addWidget(self.rating_input)

        # input box that triggers a input on 'enter' which will take in a list of tags seperated by commas as the right vbox in the bottom

        self.tag_input = QLineEdit(self)
        self.tag_input.setPlaceholderText("Enter Tag")
        self.tag_input.returnPressed.connect(self.on_tag_entered)
        self.tag_input.setFixedWidth(100)
        self.tag_input.setFixedHeight(25)
        self.tag_input.setSizePolicy(size_policy)
        self.inner_vbox.addWidget(self.tag_input)

        self.tag_list_widget = QListWidget(self)
        self.tag_list_widget.setFixedWidth(100)
        tag_list_size_policy = QSizePolicy(QSizePolicy.Policy.Fixed,
                                           QSizePolicy.Policy.Expanding)
        self.tag_list_widget.setSizePolicy(tag_list_size_policy)
        self.inner_vbox.addWidget(self.tag_list_widget)

        self.inner_hbox.addLayout(self.inner_vbox)

    def on_tag_entered(self):
        tag_text = self.tag_input.text()
        if tag_text:  # Check if the text is not empty
            self.tag_list_widget.addItem(tag_text)  # Add tag to the list widget
            self.tag_input.clear()  # Clear the input line for new input
