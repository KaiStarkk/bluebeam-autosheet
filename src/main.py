import sys
import UI
from PyQt6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    UI.style_app(app)
    w = UI.Window()
    w.show()
    sys.exit(app.exec())
