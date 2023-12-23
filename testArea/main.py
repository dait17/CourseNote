# import sys
#
# from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem
# from PyQt5.QtCore import Qt
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     lw = QListWidget()
#     for i in range(5):
#         text = f'Item {i}'
#         item = QListWidgetItem(text)
#         item.setCheckState(Qt.Unchecked)
#         lw.addItem(item)
#     lw.setDragDropMode(lw.InternalMove)
#     lw.show()
#     sys.exit(app.exec_())

import subprocess

def open_chrome_with_profile(executable_path, profile_path):
    try:
        # subprocess.run([executable_path, '--profile-directory=' + profile_path])
        subprocess.run([executable_path, '--profile-directory=' + profile_path, "https://www.google.com"])
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # Đường dẫn của Chrome
    profile_name = "Profile 2"  # Tên của profile

    open_chrome_with_profile(chrome_path, profile_name)

