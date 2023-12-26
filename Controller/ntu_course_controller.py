from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

from Models import Entities, ThoiKhoaBieu
from Views import Ui_coursePage, Ui_ntu_entry, Ui_ntu_addcourse
from PyQt5.QtWidgets import QWidget
from Models import KhoaHoc
from PyQt5.QtCore import Qt
from Controller.CustomTools import CustomData, OpenApp

import os


class NTUEntry(QWidget):
    def __init__(self):
        super(NTUEntry, self).__init__()
        self.mousePressEvent = None
        self.ui = Ui_ntu_entry()
        self.ui.setupUi(self)

        self.model: KhoaHoc | None = None

    def set_model(self, model: KhoaHoc):
        self.model = model
        self.__set_data()

    def __set_data(self):
        """
        Hiển thị dữ liệu từ model
        """
        self.ui.courseName_lb.setText(self.model.TenKH)
        self.ui.year_lb.setText(self.model.Nam)
        self.ui.semester_lb.setText(self.model.HocKy)

    def set_mouse_press(self, func):
        self.mousePressEvent = lambda event: func(self.model)


class NTUAddCourse(QWidget):
    def __init__(self):
        super(NTUAddCourse, self).__init__()
        self.ui = Ui_ntu_addcourse()
        self.ui.setupUi(self)

        self.init_data()

        self.connect_action()

    def connect_action(self):
        self.ui.year_le.textChanged.connect(self.__valid_year_input)
        self.ui.selectFolder_btn.clicked.connect(self.__select_folder)
        self.ui.folder_le.textChanged.connect(self.__valid_folder_input)
        self.ui.courseName_le_2.textChanged.connect(self.__valid_coursename)

    def init_data(self):
        self.create_semester_data()

    def create_semester_data(self):
        for s in CustomData.Semesters:
            self.ui.semester_cb.addItem(s)

    def __valid_year_input(self):
        for y in self.ui.year_le.text().split('-'):
            if not y.isdigit():
                self.ui.year_error_mess.setText("Năm không hợp lệ!")
                return False
        self.ui.year_error_mess.setText('')
        return True

    def __select_folder(self):
        self.ui.folder_le.setText(OpenApp.select_folder())

    def __is_emty_str(self, s: str):
        return len(s) == 0 or s.isspace()

    def __valid_folder_input(self):
        folder_path = self.ui.folder_le.text()
        if not self.__is_emty_str(folder_path) and not os.path.exists(folder_path):
            self.ui.warming_mess.setText(
                f'Thư mục "{folder_path}" không tồn tại. Khi nhấn lưu sẽ tiến hành tạo thư mục mới theo đường dẫn.')
            return False
        else:
            self.ui.warming_mess.setText('')
            return True

    def __valid_coursename(self):
        course_name = self.ui.courseName_le_2.text()
        if self.__is_emty_str(course_name):
            self.ui.error_mess.setText("Tên học phần không hợp lệ!")
            return False
        self.ui.error_mess.setText("")
        return True

    def valid_data(self):
        return self.__valid_coursename() and self.__valid_year_input()

    def create_folder(self):
        """
        Tạo folder mới dựa trên đường dẫn đã nhập và trả về True nếu đường dẫn thư mục rỗng hoặc thư mục đã tồn tại hoặc đã tạo thư mũ thành công, ngược lại trả về False.
        """
        folder_path = self.ui.folder_le.text()
        if self.__is_emty_str(folder_path):
            return True
        return OpenApp.create_folder(folder_path)

    def data_to_model(self):
        tenKH = self.ui.courseName_le_2.text()
        nam = self.ui.year_le.text()
        hocKy = self.ui.semester_cb.currentText()
        hocKy = hocKy if not self.__is_emty_str(self.ui.semester_cb.currentText()) else " "
        thuMuc = self.ui.folder_le.text()
        thuMuc = thuMuc if not self.__is_emty_str(thuMuc) else " "
        website = self.ui.web_le.text()
        website = website if not self.__is_emty_str(website) else " "
        return KhoaHoc(-1, tenKH, nam, hocKy, thuMuc, website)

    def set_data(self, model: KhoaHoc):
        try:
            self.ui.courseName_le_2.setText(model.TenKH)
            self.ui.year_le.setText(model.Nam)
            self.ui.semester_cb.setCurrentText(model.HocKy)
            self.ui.folder_le.setText(model.ThuMucG)
            self.ui.web_le.setText(model.WebG)
        except Exception as e:
            print(e)


class NTUCourseController(QWidget):
    def __init__(self):
        super(NTUCourseController, self).__init__()
        self.ui = Ui_coursePage()
        self.ui.setupUi(self)

        self.ui_turning()
        self.setup_ui()

        self.models = Entities()
        self.entries = []

        self.entries = self.get_entries()
        self.show_entries()

        self.addCourseQ: NTUAddCourse | None = None
        self.selected_model: KhoaHoc | None = None

    def ui_turning(self):
        self.ui.ntu_bodyContainer_lo.setAlignment(Qt.AlignTop)
        self.ui.scrollArea.setStyleSheet(
            "QScrollBar::vertical {background : #3b3e40; width: 4px;}")

    def setup_ui(self):
        """
        Thiết lập lại giao diện
        """
        self.hide_info_box()
        self.connect_action()

    def connect_action(self):
        """
        Kết nối hành động ho các nút bấm
        """
        self.ui.rm_close_btn.clicked.connect(self.hide_info_box)
        self.ui.addCourse_btn.clicked.connect(self.add_course_action)
        self.ui.rm_delcourse_btn.clicked.connect(self.remove_course)
        self.ui.rm_editCourse_btn.clicked.connect(self.edit_course_action)
        self.ui.search_le.textChanged.connect(self.__search_action)
        self.ui.rm_accessFolder_btn.clicked.connect(self.__open_folder)
        self.ui.rm_accessWeb_btn.clicked.connect(self.__open_website)

    def hide_info_box(self):
        self.ui.rightMenuContainer_w.hide()

    def show_info_box(self):
        self.ui.rightMenuContainer_w.show()

    def create_entry(self, model:KhoaHoc):
        entry = NTUEntry()
        entry.set_model(model)
        entry.set_mouse_press(self.select_entry)
        return entry

    def select_entry(self, model: KhoaHoc):
        if self.addCourseQ is None:
            self.selected_model = model

            self.ui.rm_courseName_lb.setText(model.TenKH)
            self.ui.rm_academicYear_lb.setText(model.Nam)
            self.ui.rm_semester_lb.setText(model.HocKy)
            self.ui.rm_accessWeb_btn.setToolTip(f'Mở trang web "{model.WebG}"')
            self.ui.rm_accessFolder_btn.setToolTip(f'Mở thư mục "{model.ThuMucG}"')
            self.show_info_box()
            self.show_time_of_model(model)

    def get_entries(self):
        models = self.models.KhoaHocs.to_list()
        entries = []
        for model in models:
            entry = self.create_entry(model)
            entries.append(entry)
        return entries

    def show_entries(self):
        for entry in self.entries:
            self.ui.ntu_bodyContainer_lo.addWidget(entry)

    def __set_entries(self, models):
        models.sort(key=lambda model: model.TenKH)
        self.remove_entries()
        self.entries = [self.create_entry(model) for model in models]
        self.show_entries()

    def remove_entries(self):
        for entry in self.entries:
            entry.deleteLater()

    def get_time_of_model(self, model: KhoaHoc) -> list[ThoiKhoaBieu]:
        """
        Trả danh sách đối tượng thời khoá biều của khóa học
        :return:
        """
        table = self.models.ThoiKhoaBieus
        return table.query(f'MaKH == {model.MaKH}')

    def show_time_of_model(self, model: KhoaHoc):
        models = self.get_time_of_model(model)
        if len(models) == 0:
            self.ui.rm_time_lv.setModel(None)
            return
        # Tạo mô hình dữ liệu và đặt nó cho QListView
        stan_model = QStandardItemModel(self)

        # Tạo hàng dữ liệu đầu là tên các trường dữ liệu
        head_item = QStandardItem(f"{'Thứ':<30}{'Thời gian':<30}{'Phòng':>10}")
        head_item.setBackground(QColor(204, 204, 204))
        head_item.setEditable(False)
        # Thêm hàng đầu vào mô hình dữ liệu
        stan_model.appendRow(head_item)
        for model in models:
            # Tạo các hàng dữ liệu lịch học
            stan_item = QStandardItem(
                f"{model.Thu:<30}{CustomData.time_format(model.GioBD, model.GioKT):<30}{model.Phong:>10}")
            stan_item.setEditable(False)
            # Thêm hàng dữ liệu vào mô hình dữ liệu
            stan_model.appendRow(stan_item)

        # Thêm mô hình dữ liệu vào listview
        self.ui.rm_time_lv.setModel(stan_model)

    def add_course_action(self):
        if self.addCourseQ is None:
            self.hide_info_box()
            self.addCourseQ = NTUAddCourse()
            self.addCourseQ.ui.close_btn.clicked.connect(self.close_addcourse_box)
            self.addCourseQ.ui.save_btn.clicked.connect(self.add_course)
            self.ui.mainPage_lo.addWidget(self.addCourseQ)

    def edit_course_action(self):
        try:
            self.hide_info_box()
            self.addCourseQ = NTUAddCourse()
            self.addCourseQ.set_data(self.selected_model)
            self.addCourseQ.ui.close_btn.clicked.connect(self.close_addcourse_box)
            self.addCourseQ.ui.save_btn.clicked.connect(self.edit_course)
            self.ui.mainPage_lo.addWidget(self.addCourseQ)
        except Exception as e:
            print(e)

    def close_addcourse_box(self):
        self.ui.mainPage_lo.removeWidget(self.addCourseQ)
        self.addCourseQ = None

    def reload_data(self):
        self.remove_entries()
        self.entries = self.get_entries()
        self.show_entries()
        self.hide_info_box()
        self.ui.search_le.clear()

    def save_course(self):
        self.close_addcourse_box()
        self.models.save_change()
        self.reload_data()

    def add_course(self):
        try:
            if self.addCourseQ.valid_data() and self.addCourseQ.create_folder():
                model = self.addCourseQ.data_to_model()
                model.MaKH = self.models.KhoaHocs.get_new_id()
                self.models.KhoaHocs.add(model)

                self.save_course()
        except Exception as e:
            print(e)

    def edit_course(self):
        try:
            if self.addCourseQ.valid_data() and self.addCourseQ.create_folder():
                model = self.addCourseQ.data_to_model()
                model.MaKH = self.selected_model.MaKH
                self.models.KhoaHocs.edit(model)
                self.save_course()
        except Exception as e:
            print(e)

    def remove_course(self):
        if self.selected_model is not None:
            self.models.KhoaHocs.delete(self.selected_model)
            self.save_course()

    def __search_action(self):
        text = self.ui.search_le.text()

        if len(text) == 0 or text.isspace():
            try:
                self.__set_entries(self.models.KhoaHocs.to_list())
            except Exception as e:
                print(e)
        else:
            try:
                models = self.models.KhoaHocs.search(text, ['KhoaHoc'], ['TenKH'])
                self.__set_entries(models)
            except Exception as e:
                print(e)

    def __open_folder(self):
        """
        Mở thư mục của học phần đang được chọn
        """
        if self.selected_model is not None:
            OpenApp.open_folder(self.selected_model.ThuMucG)

    def __open_website(self):
        """
        Mở Website của học phần đang được chọn
        """
        url = self.selected_model.WebG
        OpenApp.open_website(url)

