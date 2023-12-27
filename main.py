import sys
import traceback

from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtWidgets import QApplication

import MediaViewer as mv


def main():
    try:
        app = QApplication(sys.argv)
        viewer = mv.MediaViewer()
        viewer.show()
        arrow_key_filter = ArrowKeyFilter(viewer)
        app.installEventFilter(arrow_key_filter)

        path_to_media = r"P:\within temptation concert\2717271940.mp4"
        if path_to_media.endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            viewer.show_image(path_to_media)
        else:
            viewer.setPlayerMediaSource(path_to_media)
            viewer.play_video(path_to_media)

        sys.exit(app.exec())

    except Exception as e:
        print("An exception occurred:", e)
        traceback.print_exc()


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


if __name__ == "__main__":
    main()
