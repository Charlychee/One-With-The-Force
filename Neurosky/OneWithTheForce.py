from PyQt5.QtWidgets import (
	QLabel, QMainWindow, QApplication,
	QHBoxLayout, QVBoxLayout, QWidget,
	QSizePolicy, QGraphicsOpacityEffect,
	QSlider
)
from PyQt5.QtGui import QPixmap, QWindow, QMovie
from PyQt5.QtCore import Qt, QThread, QTimer
import sys
from NeuroskyWorker import NeuroskyWorker
from NeuroskyWorkerMock import NeuroskyWorkerMock


class MainWindow(QMainWindow):
	mock_data = True
	thread = None
	worker = None

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setup_ui()
		self.start_timer()
		self.start_neurosky()

		print('started_neurosky')
		# self.title = "Image Viewer"
		# self.setWindowTitle(self.title)

	def start_neurosky(self):
		self.thread = QThread()

		if self.mock_data:
			self.worker = NeuroskyWorkerMock()
		else:
			self.worker = NeuroskyWorker()

		self.worker.moveToThread(self.thread)

		# Set up threads
		self.thread.started.connect(self.worker.run)
		# self.thread_object.finished.connect(self.thread.quit)
		self.worker.finished.connect(self.worker.deleteLater)
		self.thread.finished.connect(self.thread.deleteLater)
		self.worker.opacity_signal.connect(self.update_target_opacity)

		self.thread.start()
		# print('still runs')

	def start_timer(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_opacity)

		self.timer.start(16)

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
		self.current_opacity = 0.01*(self.target_opacity - self.current_opacity)+self.current_opacity
		opacity_effect = QGraphicsOpacityEffect()
		opacity_effect.setOpacity(self.current_opacity)
		self.label.setGraphicsEffect(opacity_effect)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = MainWindow()
	w.showFullScreen()
	sys.exit(app.exec())
