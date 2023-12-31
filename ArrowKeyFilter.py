from PyQt6.QtCore import QObject, QEvent, Qt


class ArrowKeyFilter(QObject):
    def __init__(self, media_viewer):
        super().__init__()
        self.media_viewer = media_viewer
        self.VI = 0.05
        self.PI = 10000

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:

            # Fast Forward
            if event.key() == Qt.Key.Key_Right:
                self.media_viewer.position_slider.setValue(
                    self.media_viewer.position_slider.value() + self.PI)

            # Rewind
            elif event.key() == Qt.Key.Key_Left:
                self.media_viewer.position_slider.setValue(
                    self.media_viewer.position_slider.value() - self.PI)

            # Volume Up 0.05
            elif event.key() == Qt.Key.Key_Up:
                if self.media_viewer.audio_output.volume() + self.VI < 1:
                    self.media_viewer.set_volume(
                        self.media_viewer.audio_output.volume() + self.VI)
                else:
                    self.media_viewer.set_volume(1)

            # Volume Down 0.05
            elif event.key() == Qt.Key.Key_Down:
                if self.media_viewer.audio_output.volume() - self.VI > 0:
                    self.media_viewer.set_volume(
                        self.media_viewer.audio_output.volume() - self.VI)
                else:
                    self.media_viewer.set_volume(0)

            # Mute
            elif event.key() == Qt.Key.Key_M:
                if self.media_viewer.audio_output.isMuted():
                    self.media_viewer.audio_output.setMuted(False)
                else:
                    self.media_viewer.audio_output.setMuted(True)

            # Fullscreen
            elif event.key() == Qt.Key.Key_F:
                if self.media_viewer.isFullScreen():
                    self.media_viewer.showNormal()
                else:
                    self.media_viewer.showFullScreen()

            #Print window size with f strings indicating height and width
            elif event.key() == Qt.Key.Key_S:
                print(f"Height: {self.media_viewer.height()}, Width: {self.media_viewer.width()}")

        return False
