from PyQt6.QtCore import QEvent, QObject, Qt


class ArrowKeyFilter(QObject):

    def __init__(self, viewer):
        super().__init__()
        self.viewer = viewer

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Right:
                # print(f"Key pressed: {event.key()} from object {obj}")

                self.viewer.fast_forward()
                return True

            elif event.key() == Qt.Key.Key_Left:
                # print(f"Key pressed: {event.key()} from object {obj}")

                self.viewer.rewind()
                return True
        return False
