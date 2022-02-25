import pynput.keyboard
from PyQt5.QtCore import pyqtSignal, QObject
from GameplayManager import ValidAction
from pynput import keyboard
from pynput import mouse
from pynput.keyboard import Key, Controller


class KeyboardManager(QObject):
    finished = pyqtSignal()

    key_map = {"1": "[",
               "2": "]",
               "3": "/",
               "f": "-",
               "Button.right": "="}

    action = ValidAction.NONE

    pressed = set()

    def run(self):
        self.keyboard_controller: pynput.keyboard.Controller = Controller()
        self.mouse_listener = mouse.Listener(
            on_click=self.on_click)
        self.mouse_listener.start()

        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.keyboard_listener.start()

    def update_action(self, action):
        self.action = action
        self.validate_buttons()

    def on_click(self, x, y, button, pressed):
        self.process_button(str(button), pressed)

    def on_press(self, key):
        try:
            self.process_button(str(key.char), True)
        except:
            pass

    def on_release(self, key):
        try:
            self.process_button(str(key.char), False)
        except:
            pass

    def process_button(self, button: str, pressed: bool):
        if button in self.key_map:
            if pressed:
                self.press_button(button)
            else:
                self.release_button(button)

    def press_button(self, button: str):
        if self.can_press(button):
            print("Pressing" + button)
            self.keyboard_controller.press(self.key_map[button])
            self.pressed.add(button)

    def release_button(self, button: str):
        if button in self.pressed:
            self.keyboard_controller.release(self.key_map[button])
            self.pressed.remove(button)

    def can_press(self, button: str) -> bool:
        if button == "Button.right":
            return self.action >= ValidAction.BLOCK
        return self.action >= ValidAction.FORCE

    def validate_buttons(self):
        to_remove = set()
        for button in self.pressed:
            if not self.can_press(button):
                self.keyboard_controller.release(self.key_map[button])
                to_remove.add(button)
        self.pressed -= to_remove
