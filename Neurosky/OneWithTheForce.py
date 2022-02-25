from PyQt5.QtWidgets import (
    QLabel, QMainWindow, QApplication,
    QHBoxLayout, QVBoxLayout, QWidget,
    QSizePolicy, QGraphicsOpacityEffect,
    QSlider
)
from PyQt5.QtGui import QPixmap, QWindow, QMovie
from PyQt5.QtCore import Qt, QThread, QTimer, pyqtSignal
import sys
from NeuroskyWorker import NeuroskyWorker
from NeuroskyWorkerMock import NeuroskyWorkerMock
from KeyboardManager import KeyboardManager
from GameplayManager import GameplayManager, ValidAction


class MainWindow(QMainWindow):
    neurosky_thread = None
    neurosky_worker = None

    def __init__(self, parent=None, mock_data=False, refresh_rate=16):
        super().__init__(parent)
        self.refresh_rate = refresh_rate
        self.mock_data = mock_data
        self.setup_ui()
        self.start_timer()
        self.start_neurosky()

        print('started_neurosky')

    # self.title = "Image Viewer"
    # self.setWindowTitle(self.title)

    def start_neurosky(self):
        self.neurosky_thread = QThread()
        self.keyboard_manager_thread = QThread()
        self.gameplay_manager_thread = QThread()

        print(self.mock_data)
        if self.mock_data:
            self.neurosky_worker = NeuroskyWorkerMock()
        else:
            self.neurosky_worker = NeuroskyWorker()

        self.neurosky_worker.moveToThread(self.neurosky_thread)
        self.keyboard_manager_worker = KeyboardManager()
        self.gameplay_manager_worker = GameplayManager()

        self.keyboard_manager_worker.moveToThread(self.keyboard_manager_thread)
        self.gameplay_manager_worker.moveToThread(self.gameplay_manager_thread)

        # Set up threads
        self.neurosky_thread.started.connect(self.neurosky_worker.run)
        self.keyboard_manager_thread.started.connect(self.keyboard_manager_worker.run)
        self.gameplay_manager_thread.started.connect(self.gameplay_manager_worker.run)

        # self.thread_object.finished.connect(self.thread.quit)
        self.neurosky_worker.finished.connect(self.neurosky_worker.deleteLater)
        self.neurosky_thread.finished.connect(self.neurosky_thread.deleteLater)
        self.keyboard_manager_worker.finished.connect(self.keyboard_manager_worker.deleteLater)
        self.keyboard_manager_thread.finished.connect(self.keyboard_manager_thread.deleteLater)
        self.gameplay_manager_worker.finished.connect(self.gameplay_manager_worker.deleteLater)
        self.gameplay_manager_thread.finished.connect(self.gameplay_manager_thread.deleteLater)

        # Connect Signals
        self.gameplay_manager_worker.action_signal.connect(self.keyboard_manager_worker.update_action)
        self.neurosky_worker.meditation_signal.connect(self.gameplay_manager_worker.update_meditation)
        self.neurosky_worker.attention_signal.connect(self.gameplay_manager_worker.update_attention)

        self.gameplay_manager_worker.opacity_signal.connect(self.update_target_opacity)

        self.neurosky_thread.start()
        self.keyboard_manager_thread.start()
        self.gameplay_manager_thread.start()

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_opacity)

        self.timer.start(self.refresh_rate)

    def setup_ui(self):
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        # Hide Window Frame and make it stay on top
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # This works

        self.opacity_effect = QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.1)
        self.target_opacity = 0.1
        self.current_opacity = 0.1

        self.label = QLabel(self)

        self.label.setGraphicsEffect(self.opacity_effect)
        self.movie = QMovie("WispyEffectLooped.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        # Make a slider for testing

        self.label.setScaledContents(True)
        self.setCentralWidget(self.label)

    def update_target_opacity(self, opacity):
        # self.label
        self.target_opacity = opacity

    def update_opacity(self):
        self.current_opacity = 0.01 * (self.target_opacity - self.current_opacity) + self.current_opacity
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(self.current_opacity)
        self.label.setGraphicsEffect(opacity_effect)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow(mock_data=True, refresh_rate=16)
    w.showFullScreen()
    sys.exit(app.exec())
