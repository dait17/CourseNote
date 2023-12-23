# from Views import Generated
# g = Generated()
# g.generate()

from Controller.main_controller import MainController
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    # g = Generated()
    # g.generate()
    app = QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())
