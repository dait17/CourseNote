from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
import sys

# from Controller.CustomTools import tb_customtime
from Models import KhoaHoc, Entities, ThoiKhoaBieu
from Views import Ui_timeTablePage, Ui_tbEtriesForm, Ui_tb_add
from .CustomTools import *


class TBEntry(QWidget):
    def __init__(self):
        super(TBEntry, self).__init__()
        self.mousePressEvent = None
        self.ui = Ui_tbEtriesForm()
        self.ui.setupUi(self)
        self.ui_turning()

        self.model: ThoiKhoaBieu | None = None

    def ui_turning(self):
        pass
        # self.setStyleSheet('margin-top: 6px;\n')

    def append_css(self, css: str):
        old_css = self.styleSheet()
        self.setStyleSheet(old_css + '\n' + css)

    def override_css(self, new_css: str):
        self.setStyleSheet(new_css)

    def set_model(self, model: ThoiKhoaBieu):
        """
        Thiết lập dữ liệu cho mục
        """
        self.model = model
        self.__display_model()

    def __display_model(self):
        self.ui.name_lb.setText(self.model.KhoaHoc.TenKH)
        self.ui.day_lb.setText(self.model.Thu)
        self.ui.room_lb.setText(self.model.Phong)
        self.ui.lesson_lb.setText(CustomData.time_format(self.model.GioBD, self.model.GioKT))

    def set_mouse_press(self, func):
        """
        Thiết lập sự kiện click chuột vào mục
        """
        self.mousePressEvent = lambda event: func(self.model)


class TBAddTime(QWidget):
    def __init__(self):
        super(TBAddTime, self).__init__()
        self.ui = Ui_tb_add()
        self.ui.setupUi(self)

        # Khởi tạo dữ liệu
        self.__init_data()

        # self.setStyleSheet("")

        # Xử lý sự kiện
        # self.ui.selectLessonE_cb.currentIndexChanged.connect(self.nor_les_sel)

    def __init_data(self):
        self.__create_lesson_data()
        self.__create_day_data()
        self.__create_room_data()

    def __create_lesson_data(self):
        """
        Khởi tạo giá trị cho lựa chọn tiết học
        """
        for l in CustomData.lesson_range():
            self.ui.selectLessonS_cb.addItem(l, int(l))
            self.ui.selectLessonE_cb.addItem(l, int(l))

    def __create_day_data(self):
        """
        Khởi tạo giá trị cho lựa chọn thứ
        """
        for key, value in CustomData.Days.items():
            self.ui.selectDay_cb.addItem(value, int(key))
        self.ui.selectDay_cb.setCurrentIndex(1)

    def __create_room_data(self):
        """
        Khởi tạo giá trị cho ô lựa chọn phòng
        """
        for room in CustomData.Rooms:
            self.ui.selectRoom_cb.addItem(room)

    def set_data(self, model: ThoiKhoaBieu):
        self.ui.selectCourse_cb.addItem(model.KhoaHoc.TenKH, model.MaKH)
        self.ui.selectDay_cb.setCurrentText(model.Thu)
        self.set_time(model.GioBD, model.GioKT)
        self.set_lesson(model.GioBD, model.GioKT)
        self.ui.selectRoom_cb.setCurrentText(model.Phong)

    def set_lesson(self, start_time: str, end_time: str):
        """
        Nếu thời gian khớp với tiết học thì đưa dữ liệu vào ô lựa chọn tiết học, ngược lại dữ liệu để mặc định
        """
        lessons = CustomData.find_lesson_by_time(start_time, end_time)
        if lessons is not None:
            lessons.sort()
            start_lesson = lessons[0]
            end_lesson = lessons[-1]
            self.ui.selectLessonS_cb.setCurrentText(start_lesson)
            self.ui.selectLessonE_cb.setCurrentText(end_lesson)
        else:
            self.ui.selectTime_w.setCurrentIndex(1)

    def set_time(self, start_time: str, end_time: str):
        self.ui.selectTimeS_te.setTime(time(*map(int, start_time.split(':'))))
        self.ui.selectTimeE_te.setTime(time(*map(int, end_time.split(':'))))

    def get_lesson(self):
        """
        Trả về tiết học bắt đầu và tiết học kết thúc đã lựa chọn
        :return:
        """
        return self.ui.selectLessonS_cb.currentText(), self.ui.selectLessonE_cb.currentText()

    def get_time(self):
        """
        Trả về thời gian học bắt đầu và thời gian kết thúc đã lựa chọn
        :return:
        """
        return self.ui.selectTimeS_te.time().toPyTime(), self.ui.selectTimeE_te.time().toPyTime()

    def data_to_model(self):
        makh = self.ui.selectCourse_cb.currentData()
        day = self.ui.selectDay_cb.currentText()
        if self.ui.selectTime_w.currentIndex() == 0:
            # Lấy dữ liệu t ô nhập
            start_lesson = self.ui.selectLessonS_cb.currentText()
            end_lesson = self.ui.selectLessonE_cb.currentText()
            # Chuyển dữ liệu từ tiết học sang giờ
            if int(start_lesson) > int(end_lesson):
                temp = start_lesson
                start_lesson = end_lesson
                end_lesson = temp
            start = CustomData.lesson_to_time(start_lesson)
            end = CustomData.lesson_to_time(end_lesson)
            # Chuyển dữ liệu kiể str -> time
            start_time = time(*map(int, start[0].split(':')))
            end_time = time(*map(int, end[1].split(':')))
        else:
            start_time = self.ui.selectTimeS_te.time().toPyTime()
            end_time = self.ui.selectTimeE_te.time().toPyTime()
        if end_time < start_time:
            temp = time(start_time.hour, start_time.minute)
            start_time = end_time
            end_time = temp
        # Chuyển dữ liệu từ kiểu time sang kiểu str theo định dang 'Giờ:Phút'
        start_time = start_time.strftime("%H:%M")
        end_time = end_time.strftime("%H:%M")
        #
        room = self.ui.selectRoom_cb.currentText()
        if room == '':
            room = ' '
        # Lưu phòng để sau này không cần phải nhập lại
        CustomData.save_room(room)
        return ThoiKhoaBieu(-1, makh, day, start_time, end_time, room)


class TimeTableController(QWidget):
    def __init__(self):
        super(TimeTableController, self).__init__()
        self.ui = Ui_timeTablePage()
        self.ui.setupUi(self)

        # Thiết lập cho khung thêm lịch
        self.addTimeQ: TBAddTime | None = None

        # Tinh chỉnh giao diện
        self.ui_turning()
        # self.ui.rightMenuContainer.hide()
        self.__setup_rightmenu()

        # Kết nối hành động cho các nút bấm
        self.__connect_btn_actions()

        # Thêm tên các trường dữ liệu của thời gian biểu
        self.__set_head_form()

        # Data
        self.models = Entities()
        self.entries: list[TBEntry] = []
        self.reload_data()

        #
        self.selected_model: ThoiKhoaBieu | None = None

    def ui_turning(self):
        """
        (Hàm khởi tạo)
        Tinh chỉnh lại giao diện
        """
        # Ẩn khung chi tiết lịch học
        self.hide_detail_box()
        # Căn chỉnh các mục được thêm vào sẽ sắp từ trên xuống
        self.ui.tb_bodyContainer_lo.setAlignment(Qt.AlignTop)
        # Tắt thanh scroll bên dưới, chỉ hiển thị thanh bên phải khi có nhiều mục
        self.ui.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Căn chỉnh hợp khung thông tin khoá học
        self.ui.course_info_lo.setAlignment(Qt.AlignTop)

        self.ui.scrollArea.setStyleSheet(
            "QScrollBar::vertical {background : #3b3e40; width: 4px;}")

    def reload_data(self):
        self.__remove_entries()
        self.entries = self.__get_entries()
        self.__show_entries()
        self.hide_detail_box()
        self.ui.search_course_le.clear()

    def hide_detail_box(self):
        self.ui.rightMenuContainer.hide()

    def show_detail_box(self):
        self.ui.rightMenuContainer.show()

    def __connect_btn_actions(self):
        """
        (Hàm khởi tạo)
         Kết nối hành động cho các nút bấm
        """
        self.ui.rm_close_btn.clicked.connect(lambda: self.hide_detail_box())
        self.ui.addTime_btn.clicked.connect(lambda: self.add_time_action(self.models.KhoaHocs.to_list()))
        self.ui.rm_addTime_btn.clicked.connect(lambda: self.add_time_curcourse_action())
        self.ui.rm_deleteTime_btn.clicked.connect(lambda: self.__delete_time())
        self.ui.search_course_le.textChanged.connect(lambda: self.__search_action())
        self.ui.rm_folder_btn.clicked.connect(lambda: self.__open_folder())
        self.ui.rm_web_btn.clicked.connect(lambda: self.__open_web())
        self.ui.rm_editTime_btn.clicked.connect(lambda: self.edit_time_action())

    def add_time_action(self, khoaHocs: list[KhoaHoc]):
        if self.addTimeQ is None:
            widget = TBAddTime()
            widget.setStyleSheet("#tb_body {background-color: #fafafa;}")
            # Ẩn nút quay lại trên khung
            widget.ui.back_btn.hide()
            # Kết nối nút bấm
            widget.ui.close_btn.clicked.connect(self.__close_addTimeQ)
            widget.ui.saveTime_btn.clicked.connect(self.__add_time)

            # Thêm dữ liệu
            for kh in khoaHocs:
                widget.ui.selectCourse_cb.addItem(kh.TenKH, kh.MaKH)

            self.__show_addTimeQ(widget)

    def add_time_curcourse_action(self):
        try:
            if self.addTimeQ is None:
                widget = TBAddTime()
                # Ẩn nút quay lại trên khung
                widget.ui.close_btn.hide()
                # Kết nối nút bấm
                widget.ui.back_btn.clicked.connect(self.__back_addTimeQ)
                widget.ui.saveTime_btn.clicked.connect(self.__add_time)

                # # Thêm dữ liệu
                course_model = self.models.KhoaHocs.find(self.selected_model.MaKH)
                widget.ui.selectCourse_cb.addItem(course_model.TenKH, course_model.MaKH)

                self.__show_addTimeQ(widget)
        except Exception as e:
            print(e)

    def edit_time_action(self):
        model = self.selected_model
        if self.addTimeQ is None:
            widget = TBAddTime()
            widget.set_data(model)
            # Ẩn nút đóng trên khung
            widget.ui.close_btn.hide()
            # Kết nối nút bấm quay lại
            widget.ui.back_btn.clicked.connect(lambda: self.__back_addTimeQ())
            widget.ui.saveTime_btn.clicked.connect(lambda: self.__edit_time())

            self.__show_addTimeQ(widget)

    def __show_addTimeQ(self, widget: TBAddTime):
        # ẩn khung chi tiết lịch học
        self.hide_detail_box()
        # Gán khung thêm lịch mới
        self.addTimeQ = widget
        # Hiển thị khung tạo lịch
        self.ui.timeTablePage_lo.addWidget(self.addTimeQ)

    def __back_addTimeQ(self):
        self.__close_addTimeQ()
        # Hiển thị lại khung xem chi tiết lịch học
        self.show_detail_box()

    def __close_addTimeQ(self):
        self.ui.timeTablePage_lo.removeWidget(self.addTimeQ)
        self.addTimeQ = None

    def __set_head_form(self):
        """
        (Hàm khởi tạo)
        Thiết lập mục đầu tiên để hiển thị tên các trường dữ liệu trong một mục thời gian biểu
        """
        entry_head = TBEntry()
        entry_head.override_css(".QLabel {font-weight: 600;}"
                                "#mainBodyContainer{"
                                "                   border-radius: 6px;"
                                "                   background-color: #ccc;"
                                "                   margin-bottom: 6px;}"
                                "")
        entry_head.ui.name_lb.setText('Học phần')
        entry_head.ui.day_lb.setText('Thứ')
        entry_head.ui.lesson_lb.setText('Tiết')
        entry_head.ui.room_lb.setText('Phòng')
        self.ui.tb_entryHead_lo.addWidget(entry_head)

    def __setup_rightmenu(self):
        """
        (Hàm khởi tạo)
        Thiết lập lại thanh menu bên phải
        """
        # Kết nối hành động (action) cho nút đóng của thanh menu bên phải
        # self.ui.rm_close_btn.clicked.connect(lambda: self.ui.rightMenuContainer.hide())

    def __add_entry(self, et: TBEntry):
        """
        Thêm một mục thời gian biểu vào danh sách hiển thị
        """
        self.ui.tb_bodyContainer_lo.addWidget(et)

    def __remove_entry(self, et: TBEntry):
        """
        Xoá một mục ra khỏi danh sách hiển thị
        """
        if et:
            et.deleteLater()
        # self.ui.tb_bodyContainer_lo.removeWidget(et)

    def __set_entries(self, models):
        models.sort(key=lambda model: (CustomData.get_id_Thu(model.Thu), model.GioBD))
        self.__remove_entries()
        self.entries = [self.create_entry(model) for model in models]
        self.__show_entries()

    def create_entry(self, model: ThoiKhoaBieu):
        et = TBEntry()
        et.set_model(model)
        et.set_mouse_press(self.__select_entry)
        return et

    def __get_entries(self):
        entries = []

        try:
            models = self.models.ThoiKhoaBieus.to_list()
            # Sắp xếp các lịch học tăng dần theo thuộc tính Thứ và Giờ học
            # CustomData.get_id_Thu giúp lấy giá trị của Thứ theo số nguyên. VD: Thứ hai -> 2
            models.sort(key=lambda model: (CustomData.get_id_Thu(model.Thu), model.GioBD))
            for model in models:
                # et = TBEntries()
                # et.set_model(model)
                # et.set_mouse_press(self.__select_entry)
                entries.append(self.create_entry(model))
        except Exception as e:
            print(e)
        return entries

    def __select_entry(self, model: ThoiKhoaBieu):
        # Kiểm tra khung thêm thời gian chưa bật thì mới bật khung xem chi tiết
        if self.addTimeQ is None:
            self.selected_model = model
            # Thiết lập dữ liệu cảu model được chọn cho khung 'chi tiết'
            self.ui.rm_day_lb.setText(model.Thu)
            self.ui.rm_time_lb.setText(CustomData.time_format(model.GioBD, model.GioKT))

            self.ui.rm_folder_btn.setToolTip(f"Mở thư mục '{model.KhoaHoc.ThuMucG}'")
            self.ui.rm_web_btn.setToolTip(f"Mở đường dẫn '{model.KhoaHoc.WebG}'")

            self.ui.courseName_lb.setText(model.KhoaHoc.TenKH)

            # Bật hiển thị cho khung 'chi tiết'
            self.show_detail_box()

    def __show_entries(self):
        max_width = 0
        for entry in self.entries:
            self.__add_entry(entry)

    def __remove_entries(self):
        for entry in self.entries:
            self.__remove_entry(entry)

    def __save_time(self):
        self.models.save_change()
        self.reload_data()

    def __add_time(self):
        model = self.addTimeQ.data_to_model()
        model.MaTKB = Entities().ThoiKhoaBieus.get_new_id()
        self.models.ThoiKhoaBieus.add(model)
        self.__save_time()
        self.__close_addTimeQ()

    def __edit_time(self):
        model = self.addTimeQ.data_to_model()
        model.MaTKB = self.selected_model.MaTKB
        self.models.ThoiKhoaBieus.edit(model)
        self.__save_time()
        self.__close_addTimeQ()
        self.__select_entry(model)

    def __delete_time(self):
        self.models.ThoiKhoaBieus.delete(self.selected_model)
        self.__save_time()
        self.hide_detail_box()

    def __open_folder(self):
        if self.selected_model is not None:
            OpenApp.open_folder(self.selected_model.KhoaHoc.ThuMucG)

    def __open_web(self):
        if self.selected_model is not None:
            url = self.selected_model.KhoaHoc.WebG
            OpenApp.open_website(url)

    def __search_action(self):
        text = self.ui.search_course_le.text()
        time_value = [CustomData.time_format(model.GioBD, model.GioKT) for model in self.models.ThoiKhoaBieus.to_list()]

        if len(text) == 0 or text.isspace():
            try:
                self.__set_entries(self.models.ThoiKhoaBieus.to_list())
            except Exception as e:
                print(e)
        else:
            try:
                models = self.models.ThoiKhoaBieus.search(text, ['ThoiKhoaBieu', 'KhoaHoc'], ['TenKH', 'Thu', 'Phong'],
                                                          [time_value])
                self.__set_entries(models)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    # g = Generated()
    # g.generate()
    app = QApplication(sys.argv)
    window = TimeTableController()
    window.show()
    sys.exit(app.exec_())
