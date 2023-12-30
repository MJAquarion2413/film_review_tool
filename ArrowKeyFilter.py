from PyQt6.QtCore import QObject, QEvent, Qt


class ArrowKeyFilter(QObject):
    def __init__(self, media_viewer):
        super().__init__()
        self.media_viewer = media_viewer

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Right:
                self.media_viewer.fast_forward()
                return True

            elif event.key() == Qt.Key.Key_Left:
                self.media_viewer.rewind()
                return True

        return False
