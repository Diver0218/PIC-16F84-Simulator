import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

class LEDArray(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        for col in range(8):
            led = QLabel()
            led.setFixedSize(20, 20)
            led.setStyleSheet("border-radius: 10px; border: 1px solid black; background-color: #880000;")
            self.grid.addWidget(led, 0, col, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.grid)
        self.setWindowTitle("LED Array")

    def toggleLED(self, index):
        led = self.grid.itemAtPosition(0, index).widget()
        current_color = led.palette().color(led.backgroundRole())
        if current_color.red() == 136:  # Dunkles Rot
            new_color = QColor(255, 51, 51)  # Helles Rot
        else:
            new_color = QColor(136, 0, 0)  # Dunkles Rot
        led.setStyleSheet(f"border-radius: 10px; border: 1px solid black; background-color: {new_color.name()};")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LEDArray()  # Beispiel: 8x8 LED Array
    window.show()
    sys.exit(app.exec())
