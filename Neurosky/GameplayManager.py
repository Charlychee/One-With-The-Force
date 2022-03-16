from PyQt5.QtCore import pyqtSignal, QObject
import enum


class ValidAction(enum.IntEnum):
    NONE = 0
    BLOCK = 1
    FORCE = 2


class GameplayManager(QObject):
    finished = pyqtSignal()
    opacity_signal = pyqtSignal(float)
    action_signal = pyqtSignal(ValidAction)

    attention = None
    meditation = None

    def run(self):
        pass

    def update_attention(self, value):
        self.attention = value
        self.update_listeners()

    def update_meditation(self, value):
        self.meditation = value
        self.update_listeners()

    def update_listeners(self):
        self.opacity_signal.emit(self.get_opacity_from_current_state())
        self.action_signal.emit(self.get_valid_action())

    def get_valid_action(self) -> ValidAction:
        if self.attention > 60:
            return ValidAction.FORCE
        if self.attention > 50:
            return ValidAction.BLOCK
        return ValidAction.NONE

    def get_opacity_from_current_state(self) -> float:
        # Get the intensity as a percentage, then scale it
        # so it isn't as intense or distracting
        return (self.attention / 100) * 0.75
