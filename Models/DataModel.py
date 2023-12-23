from datetime import datetime, time
from Data.DataController import TableHandle

class KhoaHoc:
    def __init__(self, MaKH: int, TenKH: str, Nam: str, HocKy: int, ThuMucG: str, WebG: str):
        self.MaKH = MaKH
        self.TenKH = TenKH
        self.Nam = Nam
        self.HocKy = HocKy
        self.ThuMucG = ThuMucG
        self.WebG = WebG

    def to_dict(self):
        return {
            'MaKH': self.MaKH,
            'TenKH': self.TenKH,
            'Nam': self.Nam,
            'HocKy': self.HocKy,
            'ThuMucG': self.ThuMucG,
            'WebG': self.WebG
        }


class ThoiKhoaBieu:
    def __init__(self, MaTKB: int, MaKH: int, Thu: str, GioBD: str, GioKT: str, Phong: str):
        self.MaTKB = MaTKB
        self.MaKH = MaKH
        self.Thu = Thu
        self.GioBD = GioBD
        self.GioKT = GioKT
        self.Phong = Phong

        # Đối tượng khoá ngoại
        self.KhoaHoc = None

        self.setup_foreign_oj()

    def setup_foreign_oj(self):
        k = TableHandle('KhoaHoc').find("MaKH", self.MaKH)
        self.KhoaHoc = KhoaHoc(**k.iloc[0].to_dict())

    def to_dict(self):
        return {
            'MaTKB': self.MaTKB,
            'MaKH': self.MaKH,
            'Thu': self.Thu,
            'GioBD': self.GioBD,
            'GioKT': self.GioKT,
            'Phong': self.Phong
        }

