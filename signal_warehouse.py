from PySide6.QtCore import QObject, Signal


class SignalWarehouse(QObject):
    # Define signals here
    # Example: play_video = Signal(str)

    def __init__(self):
        super().__init__()
        self.connections = {}

    def register_signal(self, signal_name, signal):
        setattr(self, signal_name, signal)

    def connect_signal(self, emitter, signal_name, receiver):
        signal = getattr(self, signal_name, None)
        if signal:
            emitter.connect(signal.connect(receiver))

    def disconnect_signal(self, emitter, signal_name, receiver):
        signal = getattr(self, signal_name, None)
        if signal:
            emitter.disconnect(signal.disconnect(receiver))
