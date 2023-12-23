import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QRegExp, QThread, pyqtSignal
from PyQt5 import QtCore
import pandas as pd

class DataFrameLoader(QThread):
    data_loaded = pyqtSignal(pd.DataFrame)

    def __init__(self):
        super().__init__()

    def run(self):
        # Tải dữ liệu từ nguồn nào đó
        # data = {'Name': ['John', 'Jane', 'Sam', 'Sara'],
        #         'Age': [28, 24, 22, 32],
        #         'City': ['New York', 'Toronto', 'Paris', 'London']}
        # for i in range(1000):  # Tạo thêm dữ liệu để kiểm tra phân trang
        #     data['Name'].extend(['Name{}'.format(i) for i in range(4)])
        #     data['Age'].extend([i for i in range(4)])
        #     data['City'].extend(['City{}'.format(i) for i in range(4)])

        df = pd.read_csv(r'D:\Workspace\NTU_project\LapTrinhPython\WorkNote\testArea\test.csv')
        self.data_loaded.emit(df)

class DataFrameViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Tạo QTableView và thiết lập model cho nó
        self.table_view = QTableView(self)
        self.model = PandasModel(pd.DataFrame())
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setModel(self.proxy_model)

        # Tạo ô tìm kiếm
        self.search_label = QLabel('Search:')
        self.search_edit = QLineEdit(self)
        self.search_edit.textChanged.connect(self.filter_table)

        # Tạo đối tượng loader và kết nối tín hiệu
        self.data_loader = DataFrameLoader()
        self.data_loader.data_loaded.connect(self.on_data_loaded)

        # Đặt QTableView làm widget chính
        central_widget = QWidget(self)
        central_layout = QVBoxLayout(central_widget)
        central_layout.addWidget(self.search_label)
        central_layout.addWidget(self.search_edit)
        central_layout.addWidget(self.table_view)
        self.setCentralWidget(central_widget)

        # Thiết lập cấu hình cho QTableView
        self.table_view.setSortingEnabled(True)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        self.table_view.horizontalHeader().setStretchLastSection(True)

        # Bắt đầu quá trình tải dữ liệu
        self.data_loader.start()

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('DataFrame Viewer')
        self.show()

    def on_data_loaded(self, data_frame):
        # Khi dữ liệu đã được tải, cập nhật model
        self.model = PandasModel(data_frame)
        self.proxy_model.setSourceModel(self.model)
        self.table_view.setModel(self.proxy_model)

    def filter_table(self):
        filter_text = self.search_edit.text()
        regex = QRegExp(filter_text, Qt.CaseInsensitive, QRegExp.RegExp)
        self.proxy_model.setFilterKeyColumn(-1)  # -1 để tìm kiếm trên toàn bộ các cột
        self.proxy_model.setFilterRegExp(regex)
        self.table_view.resizeColumnsToContents()

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, data_frame):
        super().__init__()
        self.data_frame = data_frame

    def rowCount(self, parent=None):
        return self.data_frame.shape[0]

    def columnCount(self, parent=None):
        return self.data_frame.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.data_frame.iloc[index.row(), index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return str(self.data_frame.columns[section])
        return None

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Hiển thị DataFrame bằng cách sử dụng lớp DataFrameViewer
    viewer = DataFrameViewer()

    sys.exit(app.exec_())
