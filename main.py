import sys
from PyQt6.QtWidgets import QApplication, QFileDialog
import BaseGUI as bg


def center_width(base_gui):
    #TODO fix this to center frame on screen
    window_size = base_gui.geometry()
    center_x = (1280 - window_size.width()) // 2
    base_gui.move(center_x, 0)


def main():
    # try:
    app = QApplication(sys.argv)
    viewer = bg.BaseGUI()
    viewer.setup_media_selector()
    # make a qdialog to open a folder popup
    folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
    viewer.set_initial_file(folder_path)
    center_width(viewer)
    viewer.show()

    print("Setting Initial File Opened")

    sys.exit(app.exec())


# except Exception as e:
#    print("An exception occurred:", e)
# Handle or log the exception as needed


if __name__ == "__main__":
    main()
