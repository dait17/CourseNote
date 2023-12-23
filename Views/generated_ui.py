import os, sys
from time import sleep


class Generated:
    def __init__(self):
        self.ui_file_list = Generated.get_all_ui_file()
        self.qrc_file_list = self.get_all_qrc_file()
        self.package_path = Generated.get_package_path()

    def generate(self):
        self.generate_ui()
        self.generate_qrc()
        self.fix_file()
        # os.system('exit()\ncd ..\npython main.py')

    def generate_ui(self):
        for f in self.ui_file_list:
            path_ui = os.path.join(self.package_path, f)
            path_py = os.path.join(self.package_path, f.replace('.ui', '.py'))
            os.system(f'pyuic5 {path_ui} -o {path_py}')

    def fix_file(self):
        # file_list = ['main_layout.py', 'timeTable.py']
        file_list = Generated.get_all_py_file()
        file_list.remove('generated_ui.py')
        for f in file_list:
            path = os.path.join(self.package_path, f)
            with open(path, 'r', encoding='utf-8') as file:
                file = file.read()
            content = file.replace('import resources_rc', 'from Views import resources_rc')
            with open(path, 'w', encoding='utf-8') as file:
                file.write(content)

    def generate_qrc(self):
        for f in self.qrc_file_list:
            path_ui = os.path.join(self.package_path, f)
            path_py = os.path.join(self.package_path, f.replace('.qrc', '_rc.py'))
            os.system(f'pyrcc5 {path_ui} -o {path_py}')



    @staticmethod
    def get_package_path():
        return os.path.dirname(__file__)

    @staticmethod
    def get_all_ui_file():
        return Generated.get_file('.ui')

    @staticmethod
    def get_all_py_file():
        return Generated.get_file('.py')

    @staticmethod
    def get_all_qrc_file():
        return Generated.get_file('.qrc')

    @staticmethod
    def get_file(ex:str):
        return [f for f in os.listdir(Generated.get_package_path()) if ex in f]


if __name__ == '__main__':
    print(Generated.get_all_ui_file())

