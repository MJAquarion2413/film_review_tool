import sys
from PyQt6.QtWidgets import QApplication
import BaseGUI as bg


def center_width(base_gui):
    window_size = base_gui.geometry()
    center_x = (1280 - window_size.width()) // 2
    base_gui.move(center_x, 0)


def main():
    # try:
    app = QApplication(sys.argv)
    viewer = bg.BaseGUI()
    viewer.show()
    viewer.setup_media_selector()
    print("Setting Initial File Opened")
    viewer.check_if_objects_exists()
    viewer.set_initial_file()
    center_width(viewer)

    sys.exit(app.exec())


# except Exception as e:
#    print("An exception occurred:", e)
# Handle or log the exception as needed


if __name__ == "__main__":
    main()
