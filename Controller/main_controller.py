from Views import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from Controller import TimeTableController, NTUCourseController


class MainController(QMainWindow):
    def __init__(self):
        super(MainController, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Thiết lập giao diện
        self.setup_ui()

    def setup_ui(self):
        """
        Thiết lập gian diện
        """
        self.add_page()
        self.connect_action()

    def add_page(self):
        """
        Thêm các trang vào giao diện chính
        """
        self.timetable_ui = TimeTableController()
        self.ui.bodyContainer.addWidget(self.timetable_ui)

        self.ntucourse_ui = NTUCourseController()
        self.ui.bodyContainer.addWidget(self.ntucourse_ui)

    def connect_action(self):
        """
        Kết nối hành động cho các nút bấm
        """
        # Kết nối nút bấm 'Thòi gian biểu'
        self.ui.timeTable_btn.clicked.connect(lambda: self.set_current_page(0))

        self.ui.ntuCourses_btn.clicked.connect(lambda: self.set_current_page(1))

    def set_current_page(self, id: int):
        """
        Thiết lập ttang hiện tại dựa trên chỉ mục của các trang
        """
        self.ui.bodyContainer.setCurrentIndex(id)
        self.ui.bodyContainer.currentWidget().reload_data()
