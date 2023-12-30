from PyQt6.QtWidgets import QSlider
from PyQt6.QtCore import Qt


class ClickableSlider(QSlider):
    def __init__(self, orientation, media_viewer=None, parent=None):
        super().__init__(orientation, parent)
        self.media_viewer = media_viewer

    def mousePressEvent(self, event):
        # Calculate the slider value based on mouse position
        if event.button() == Qt.MouseButton.LeftButton:
            value = self.minimum() + ((self.maximum() - self.minimum()) * event.position().x()) / self.width()
            self.blockSignals(True)
            self.setValue(int(value))
            if self.media_viewer:
                self.media_viewer.set_position(int(value))
            self.blockSignals(False)
            event.accept()
        else:
            super().mousePressEvent(event)
