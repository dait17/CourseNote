from Models.DataModel import *


class DataTable:
    def __init__(self, table_name: str):
        self.__data = TableControl(table_name)

    def query(self, q: str):
        try:
            result = self.__data.table.query(q)
        except:
            return []
        models = []
        for index, row in result.iterrows():
            models.append(DataTable.to_model(self.__data.table_name, row.to_dict()))
        return models

    def search(self, value, tables: list[str], cols: list[str], custom_col_value: list[list] | None = None):
        """
        Tìm kiếm dựa trên các bảng và trường dữ liệu được truyền vào. Trả về một danh sách các model của bảng hiện tại.
        :param value: giá trị tìm kiếm
        :param tables: tên các bảng dữ liệu
        :param cols: tên các trường dữ liệu
        :param custom_col_value: cột dữ liệu tự định nghĩa
        :return: 
        """
        data = self.__data.search(value, tables, cols, custom_col_value)
        result = []
        for index, row in data.iterrows():
            m = DataTable.to_model(self.__data.table_name, self.__data.collect_data(row))
            result.append(m)
        return result

    def get_new_id(self):
        """
        Trả về mã kế tiếp của mã cuối cùng, dùng để tạo mã mới.
        :return:
        """
        return self.__data.get_new_id()

    def add(self, model):
        self.__data.add(model.to_dict())

    def edit(self, model):
        self.__data.edit(model.to_dict())

    def delete(self, model):
        self.__data.delete(model.to_dict())

    def to_list(self):
        models = []
        tb_name = self.__data.table_name
        for i in self.__data.table.index:
            data = self.__data.table.loc[i]
            models.append(DataTable.to_model(tb_name, data.to_dict()))
        return models

    def find(self, id: str):
        """
        Trả về một model khớp với khoá chính, nếu không trả về None
        :return:
        """
        key = self.__data.get_primary_key()[0]
        data = self.__data.find(key, id)
        if not data.empty:
            return DataTable.to_model(self.__data.table_name, data.iloc[0].to_dict())
        return None

    def save_change(self):
        self.__data.save_change()

    def __str__(self):
        return self.__data.table.to_string()

    @staticmethod
    def to_model(table_name: str, data: dict):
        if table_name == 'KhoaHoc':
            return KhoaHoc(**data)
        if table_name == 'ThoiKhoaBieu':
            return ThoiKhoaBieu(**data)


if __name__ == '__main__':
    model = DataTable('KhoaHoc')
    print(model.get_new_id())
