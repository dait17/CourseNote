from .Conversion import *


class Entities:
    def __init__(self):
        self.KhoaHocs = DataTable('KhoaHoc')
        self.ThoiKhoaBieus = DataTable('ThoiKhoaBieu')

    def save_change(self):
        self.KhoaHocs.save_change()
        self.ThoiKhoaBieus.save_change()

