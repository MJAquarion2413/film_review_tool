import importlib
import json

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDockWidget

from signal_warehouse import SignalWarehouse


class ComponentManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.signal_warehouse = SignalWarehouse()
        self.components = {}
        self.config_path = 'layout_config.json'
        self.load_config()

    def load_config(self):
        with open(self.config_path, 'r') as file:
            self.config = json.load(file)

    def load_components(self):
        for entry in self.config['layout']:
            widget_class = entry['widget']
            position = entry['position']
            features = entry['features']
            settings = entry.get('settings', {})
            self.load_widget(widget_class, position, features, settings)

    def load_widget(self, widget_class_name, position, features, settings):
        module_path = f"Display_Components.{widget_class_name.lower()}"
        widget_module = importlib.import_module(module_path)
        widget_class = getattr(widget_module, widget_class_name)
        widget_instance = widget_class(self.signal_warehouse)

        if position == 'central':
            self.main_window.setCentralWidget(widget_instance)
        elif position.startswith('dock:'):
            dock_area = position.split(':')[1]
            dock_widget = QDockWidget(self.main_window)
            dock_widget.setWidget(widget_instance)
            dock_widget.setFeatures(self.parse_dock_features(settings.get('dockFeatures', '')))
            self.add_dock_widget(dock_widget, dock_area)
        else:
            raise Exception(f"UPDATE NON-DOCK/NON-CENTRAL WIDGET LOADING")

        self.components[widget_class_name] = widget_instance

    def parse_dock_features(self, features_str):
        features = QDockWidget.DockWidgetFeature(0)
        if 'closable' in features_str:
            features |= QDockWidget.DockWidgetFeature.DockWidgetClosable
        return features

    def add_dock_widget(self, dock_widget, dock_area):
        area_dict = {
            'left': Qt.DockWidgetArea.LeftDockWidgetArea,
            'right': Qt.DockWidgetArea.RightDockWidgetArea,
            'top': Qt.DockWidgetArea.TopDockWidgetArea,
            'bottom': Qt.DockWidgetArea.BottomDockWidgetArea
        }
        self.main_window.addDockWidget(area_dict[dock_area], dock_widget)
