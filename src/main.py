import sys

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QVBoxLayout, QWidget)


# Worker Thread for Data Acquisition
class DataThread(QThread):
    data_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        t = 0
        while self.running:
            t += 0.1
            data = np.sin(2 * np.pi * 1 * t) + np.random.normal(0, 0.1)
            self.data_signal.emit(np.array([data]))
            self.msleep(50)  # Simulate 20Hz update rate

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

# Main GUI Class
class WaveformApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-time Waveform GUI")
        self.setGeometry(100, 100, 800, 600)

        self.plot_widget = pg.PlotWidget()
        self.plot_data = self.plot_widget.plot([], pen='y')
        self.data_buffer = []

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start_acquisition)

        self.stop_btn = QPushButton("Stop")
        self.stop_btn.clicked.connect(self.stop_acquisition)

        layout = QVBoxLayout()
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.plot_widget)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.data_thread = DataThread()
        self.data_thread.data_signal.connect(self.update_plot)

    def start_acquisition(self):
        if not self.data_thread.isRunning():
            self.data_thread = DataThread()
            self.data_thread.data_signal.connect(self.update_plot)
            self.data_thread.start()

    def stop_acquisition(self):
        self.data_thread.stop()

    def update_plot(self, data):
        self.data_buffer.append(data[0])
        if len(self.data_buffer) > 500:
            self.data_buffer.pop(0)
        self.plot_data.setData(self.data_buffer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WaveformApp()
    window.show()
    sys.exit(app.exec())
