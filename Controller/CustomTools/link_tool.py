import tkinter as tk
from tkinter import messagebox, filedialog
import os
import subprocess
import webbrowser


class OpenApp:
    def __init__(self):
        pass

    @staticmethod
    def check_folder_path(path: str):
        try:
            if len(path) == 0 or path.isspace():
                OpenApp.show_error_dialog("Đường dẫn thư mục trống!")
                return False
            if not os.path.exists(path):
                OpenApp.show_error_dialog("Thư mục không tồn tại!")
                return False
        except:
            OpenApp.show_error_dialog("Không mở được thư mục!")
            return False
        return True

    @staticmethod
    def create_folder(folder_path):
        """
        Tạo folder mới dựa trên đường được truyenf vào, trả về True nếu đường dẫn thư mục đã tồn tại hoặc đã tạo thư mục thành công, ngược lại trả về False.
        """
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                return True
            except Exception as e:
                OpenApp.show_error_dialog(f'Không thể tạo thư mục "{folder_path}": {e}')
                return False
        return True

    @staticmethod
    def show_error_dialog(mess: str):
        root = tk.Tk()
        root.withdraw()  # Ẩn cửa sổ chính của Tkinter
        # Hiển thị hộp thoại thông báo lỗi
        messagebox.showerror("Lỗi", mess)

    @staticmethod
    def open_folder(folder_path: str):
        """
        Mở thư mục theo đường dẫn thư mục được truyền vào.
        """
        if OpenApp.check_folder_path(folder_path):
            try:
                folder_path = folder_path.replace('/', '\\')
                subprocess.run(['explorer', folder_path])
            except Exception as e:
                OpenApp.show_error_dialog(e.__str__())

    @staticmethod
    def open_website(url: str):
        """
        Mở trang web bằng trình duyệt mặc định dựa trên url được truyền vào
        """
        try:
            if not (len(url) == 0 or url.isspace()):
                OpenApp.__open_web_by_default_browser(url)
        except Exception as e:
            OpenApp.show_error_dialog("Không thẻ mở trang web, lỗi đường dẫn!")

    @staticmethod
    def __open_web_by_default_browser(url):
        try:
            webbrowser.open(url)
        except Exception as e:
            OpenApp.show_error_dialog(e.__str__())

    @staticmethod
    def select_folder():
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory()
        return folder_path


if __name__ == '__main__':
    print(OpenApp.open_folder(r'D:/Ảnh'))
