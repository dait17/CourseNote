from Data.DataController import DataControl, DataTable
from DataBase import Entities
from DataModel import KhoaHoc, LoaiKhoaHoc
import datetime


# def add_lkh():
#     a = LoaiKhoaHocs()
#     model = LoaiKhoaHoc(1, 'Học phần')
#     print(a)
#     a.add(model)
#     print(a)
#     a.save_change()
#
#
# def add_kh():
#     a = KhoaHocs()
#     model = KhoaHoc(1, 'Thử nghiệm', datetime.datetime.now(), datetime.datetime.now(), '', '', 1)
#     print(a)
#     a.add(model)
#     print(a)
#     a.save_change()


# def edit_kh():
#     a = KhoaHocs()
#     model = KhoaHoc(1, 'Đổi tên lần nữa', datetime.datetime.now(), datetime.datetime.now(), None, None, 1)
#     print(a)
#     a.edit(model)
#     print(a)
#     a.save_change()


if __name__ == '__main__':
    start = datetime.datetime.now()

    #
    db = Entities()
    # model = KhoaHoc(1, 'Thử nghiệm', datetime.datetime.now(), datetime.datetime.now(), '', '', 1)
    # db.KhoaHocs.add(model)
    print(len(db.KhoaHocs.to_list()))
    # db.save_change()
    #

    end = datetime.datetime.now()
    print(end - start)
    # while 1:
    #     a = input('>> ')
    #     a = a.replace("'","")
    #     print(a)
    #     for s in a.split(','):
    #         print(f"self.{s} = {s}")
