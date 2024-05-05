from PySide6.QtWidgets import QApplication, QMainWindow
import sys

from component_manager import ComponentManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Manager")

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()

    component_manager = ComponentManager(main_window)
    component_manager.load_components()

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
