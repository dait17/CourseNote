import os
import pandas as pd

package_path = os.path.dirname(__file__)


class DataControl:
    """
    Class chiệu trách nhiệm tương tác trục tiếp với dữ liệu được lưu dưới dạng file csv.
    Giúp đảm bảo tính đúng đắn của cơ sở dữ liệu.
    Các tham số truyền vào dạng table_name, hoặc file_name phải có đuôi .csv
    """

    __TableStruc = {
        'KhoaHoc.csv': {
            'cols': ['MaKH', 'TenKH', 'Nam', 'HocKy', 'ThuMucG', 'WebG'],
            'primary_key': ['MaKH'],
            'foreign_key': []
        },
        'ThoiKhoaBieu.csv': {
            'cols': ['MaTKB', 'MaKH', 'Thu', 'GioBD', 'GioKT', 'Phong'],
            'primary_key': ['MaTKB'],
            'foreign_key': [['MaKH', 'KhoaHoc.csv', 'MaKH']]
        }
    }

    @staticmethod
    def __get_all_file() -> list:
        """
        Trả về danh sách tên các file csv được chứa trong package Data
        :return:
        """
        return [f for f in os.listdir(package_path) if '.csv' in f]

    @staticmethod
    def get_table_struc(table_name: str):
        table = DataControl.__TableStruc.get(table_name)
        if table is not None:
            return table
        raise "Table not found in the data structure!"

    @staticmethod
    def get_primary_key(table_name: str):
        table = DataControl.get_table_struc(table_name)
        return table.get('primary_key')

    @staticmethod
    def get_foreign_key(table_name: str):
        table = DataControl.get_table_struc(table_name)
        return table.get('foreign_key')

    @staticmethod
    def get_table_cols(table_name: str):
        table = DataControl.get_table_struc(table_name)
        return table.get('cols')

    @staticmethod
    def get_all_table_name():
        return list(DataControl.__TableStruc.keys())

    @staticmethod
    def __create_table(table_name: str):
        # Lấy các trường dữ liệu của bảng (Header)
        cols = DataControl.get_table_cols(table_name)
        # Tạo dataFrame (dữ liêu mẫu)
        data = {}
        for col in cols:
            data.update({col: []})

        df = pd.DataFrame(data)
        # Lưu file
        filePath = os.path.join(package_path, table_name)
        df.to_csv(filePath, index=False, header=True)

    @staticmethod
    def __get_file_path(file_name: str):
        return os.path.join(package_path, file_name)

    @staticmethod
    def __read_csv(file_path):
        """
        Đọc file csv theo đường dẫn tuyệt đối đường truyền vào
        :param file_path:
        """
        return pd.read_csv(file_path, header=0, encoding='utf-8')

    @staticmethod
    def read_table(table_name: str):
        """
        Đọc và trả về dữ liệu từ file csv
        :param table_name:
        :return:
        """
        file_path = DataControl.__get_file_path(table_name)
        # Thử tìm file, nếu có trả về dữ liệu đã chuyển đổi thành kiểu DataFrame
        # nếu xảy ra lỗi, tiến hành xử lý lỗi
        try:
            return DataControl.__read_csv(file_path)
        except FileNotFoundError:
            # Nếu file có trong mẫu cơ sở dữ liệu nhưng không ở trong package Data
            # #thì tiến hành tạo file mới, ngược lại báo lỗi
            if table_name in DataControl.get_all_table_name():
                DataControl.__create_table(table_name)
                return DataControl.__read_csv(file_path)
            else:
                raise "Table not found in the database!"

    @staticmethod
    def __is_duplicate(table_name: str, table_data: pd.DataFrame):
        """
        Kiểm tra khoá chính của bảng có bị trùng lặp không, nếu có trả về True, ngược lại trả về False
        :return:
        """
        primary_key = DataControl.get_primary_key(table_name)
        return table_data[primary_key].duplicated().any()

    @staticmethod
    def find_lose_key(table1: pd.DataFrame, col_name1: str, table2: pd.DataFrame, col_name2: str) -> pd.Series:
        """
        Trả về dữ liệu có ở col_name1 table1 nhưng không có trong col_name2 table2
        :return:
        """
        return table1.loc[~table1[col_name1].isin(table2[col_name2]), col_name1]

    @staticmethod
    def __is_foreignkey_existed(table_name: str, table_data: pd.DataFrame):
        foreign_keys = DataControl.get_foreign_key(table_name)

        for key in foreign_keys:
            # Lấy dữ liệu của bảng hiện tại
            cur_col = table_data[[key[0]]]

            # Lấy dữ liệu của bảng chứa khoá ngoại
            fore_col = DataControl.read_table(key[1])[[key[2]]]

            # Lấy giá trị có trong bảng hiện tại nhưng không có trong bảng chứa khoá ngoại
            cur_not_in_fore = cur_col.loc[~cur_col[key[0]].isin(fore_col[key[2]]), key[0]]
            if len(cur_not_in_fore.index) > 0:
                return False
        return True

    @staticmethod
    def write_table(table_name: str, table_data: pd.DataFrame):
        """
        Ghi file csv
        :param table_name:
        :param table_data:
        :return:
        """
        if DataControl.__is_duplicate(table_name, table_data):
            raise 'Error: Duplicate key!'
        if not DataControl.__is_foreignkey_existed(table_name, table_data):
            raise 'Error: data mismatch with foreign key!'
        file_path = DataControl.__get_file_path(table_name)
        table_data.to_csv(file_path, index=False, header=True, encoding='utf-8')


class TableControl:
    __AllTableData = {}

    def __init__(self, table_name: str):
        self.table_name = table_name
        self.table = TableControl.get_table(table_name)

    def get_primary_key(self):
        return DataControl.get_primary_key(self.table_name + '.csv')

    def get_cols(self):
        return DataControl.get_table_cols(self.table_name + '.csv')

    def get_new_id(self):
        try:
            if self.table[self.get_primary_key()[0]].count() == 0:
                return 1
            return max(self.table[self.get_primary_key()[0]].tolist()) + 1
        except:
            return -1

    def add(self, model: dict):
        l = len(self.table.index)
        self.table.loc[l] = model

    def collect_data(self, series: pd.Series):
        cols = self.get_cols()
        d = {}
        for col in cols:
            d.update({col: series[col]})
        return d

    def find_model(self, model: dict):
        """
        Trả về 1 DataFrame chứa hàng đầu tiên khớp với dữ liệu từ model
        :param model:
        """
        primary_key = DataControl.get_primary_key(self.table_name + '.csv')
        # Tìm hàng cần thay đổi dựa trên trường dữ liệu đầu tiên của khoá chính
        rows = self.table[self.table[primary_key[0]] == model.get(primary_key[0])]

        # Tìm hàng cần thay đổi dựa trên các trường dữ liệu còn lại của khoá chính
        for k in range(1, len(primary_key)):
            rows = rows[rows[primary_key[k]] == model.get(primary_key[k])]
        return rows.iloc[[0], :]

    def find(self, col: str, value: any):
        """
        Tìm và trả về dữ liệu khớp với giá trị của cột tại bảng được truyền vào
        :return:
        """
        table = TableControl.get_table(self.table_name)
        return table[table[col] == value]

    def search_data(self, value):
        """
        Tìm kiếm dựa trên toàn bộ các trường của của bảng hiện tại.
        :return:
        """
        table = TableControl.get_table(self.table_name)
        str_table = table.astype(str)
        data = pd.DataFrame({})
        primary_key = self.get_primary_key()
        cols = DataControl.get_table_cols(self.table_name + '.csv')
        for col in cols:
            try:
                result = str_table[str_table[col].str.contains(str(value))]
                data = pd.concat([data, result])
            except Exception as e:
                print(e)
        data = data.drop_duplicates()
        return table.loc[table[primary_key[0]].isin(list(map(int, data[primary_key[0]].to_list())))]

    def search(self, value: any, tables: list[str], cols: list[str], custom_col_value: list[list] | None = None):
        """
        Tìm kiếm dựa trên các bảng và trường dữ liệu được truyền vào.
        :param value: Giá tị cần tìm
        :param tables: Tên các bảng
        :param cols: Tên các cột
        :param custom_col_value: hàng dữ liệu tự định nghĩa
        :return:
        """
        # Khởi tạo một dataframe rỗng để chứa dữ liệu khớp với giá trị tìm kiếm
        search_data = pd.DataFrame({})
        if len(cols) == 0 or len(tables) == 0 or value is None:
            return search_data

        # Chuyển giá trị tìm kiếm thành kiểu string để tìm kiếm
        value = str(value).lower()

        # Kết hợp các bảng được
        data = TableControl.inner_join(*tables)

        # Thêm các cột dữ liệu tự định nghĩa
        if custom_col_value is not None:
            for index, col in enumerate(custom_col_value):
                if col is not None or len(col) != 0:
                    data[f'custom_col_{index}'] = col
                    cols.append(f'custom_col_{index}')

        # Thiết lập khoá chính cho toàn bộ dữ liệu được kết hợp từ các bảng
        data['pri_key'] = list(range(len(data)))

        # Tạo một bảng tạm để chứa dữu liệu của toàn bộ các bảng đã được chuyển đổi
        # sang kiểu string và kiểu in thường (lower)
        data_to_str = data.astype(str)
        data_to_str = data_to_str.map(str.lower)

        ## Quy trình tìm kiếm
        # 1. Duyệt qua từng cột dữ liệu và lấy các giá trị trông cột có chứa giá trị cần tìm,
        # sau đó thêm vào 'search_data'
        # 2. Chuyển dữ liệu của cột 'pri_key' từ str -> int,
        # sau đó so khớp với dữ liệu bang đầu được lưu trong data và
        # trả về một phiên bảng dữ liệu chứa toàn bộ các bảng đã được kết hợp có chứa giá trị cần tìm
        for col in cols:
            try:
                result = data_to_str[data_to_str[col].str.contains(value)]
                search_data = pd.concat([search_data, result])
            except Exception as e:
                print(e)
        search_data = search_data.drop_duplicates()

        search_data = data.loc[data['pri_key'].isin(list(map(int, search_data['pri_key'].to_list())))]
        return search_data

    @staticmethod
    def inner_join(*table_name):
        # Danh sách tên các bảng đã join
        data_tn = []
        # dữ liệu được join từ các bảng
        data = pd.DataFrame({})
        # Duyệt qua tất cả các bảng cần join
        for tn in table_name:
            # Lấy tên thuộc tính khoá ngoại và tên bảng chứa khoá ngoại
            # Hàm 'get_foreign_key' trả về một mảng 2 chiều, với mỗi mảng 1 chiều bên trong chứa các thuộc tính:
            # [tên cột khoái ngoại trong bảng, tên bảng chính chứa khoá ngoại, tên cột trong bảng chính]
            foreign_table = DataControl.get_foreign_key(tn + '.csv')
            if len(data_tn) == 0 and len(foreign_table) == 0:
                data_tn.append(tn)
                data = TableControl.get_table(tn).copy()

            # Duyệt qua từng khoá ngoại,
            # nếu bảng chứa khoá ngoại có trong danh sách các bảng cần join và bảng chưa được join thì thực hiện join
            for fk in foreign_table:
                ftb = fk[1].replace('.csv', '')
                # Kiểm tra bảng đã có trong danh sách các bảng được join chưa
                # if (ftb in table_name) and (ftb not in data_tn):
                if tn not in data_tn or ftb not in data_tn:
                    tbl = TableControl.get_table(tn).copy()
                    tbr = TableControl.get_table(ftb).copy()
                    new_data = pd.merge(tbl, tbr, left_on=fk[0], right_on=fk[2], how='inner')
                    if len(data_tn) == 0:
                        data = new_data.copy()
                        data_tn.extend([tn, ftb])
                    else:
                        if tn in data_tn and ftb not in data_tn:
                            # primary_key = DataControl.get_primary_key(ftb + '.csv')
                            data = pd.merge(data, tbr, left_on=fk[0], right_on=fk[2], how='inner')
                            data_tn.append(ftb)
                        elif ftb in data_tn and tn not in data_tn:
                            # primary_key = DataControl.get_primary_key(tn + '.csv')
                            data = pd.merge(data, tbl, left_on=fk[2], right_on=fk[0], how='inner')
                            data_tn.append(tn)
        return data

    def edit(self, model: dict):
        row_edit = self.find_model(model)
        # Nếu hàng cần sửa đổi không rỗng tiến hành thay đổi dữ liệu
        if not row_edit.empty:
            # Lấy chỉ mục hàng đầu tiên

            row_index = row_edit.index[0]

            for col in DataControl.get_table_cols(self.table_name + '.csv'):
                self.table.at[row_index, col] = model.get(col)

            return
        raise "Eror: Primary key does not exist in the database!"

    def delete(self, model: dict):
        rows = self.find_model(model)
        for i in rows.index.tolist():
            self.table.drop(i, inplace=True)
        self.table.reset_index(drop=True, inplace=True)

    def save_change(self):
        TableControl.update(self.table_name, self.table)

        # cập nhật lại dữ liệu cho bảng
        self.table = self.get_table(self.table_name)

    @staticmethod
    def clean_data(table_name: str, table_data: pd.DataFrame):
        """
        Xoá các mục dữ liệu được đọc từ file csv có khoá ngoại không khớp
        :return:
        """
        foreign_key = DataControl.get_foreign_key(table_name + '.csv')
        for key in foreign_key:
            # Lấy dữ liệu từ bảng chứa khoá ngoại
            forei_table = DataControl.read_table(key[1])
            # Lấy dữ liệu có trong cột kết nối khoá ngoại của bảng hiện tại nhưng không có trong bảng chứa khoá ngoại
            cur_not_in_fore = DataControl.find_lose_key(table_data, key[0], forei_table, key[2])
            # xoá các bản ghi không hợp lệ
            for i in cur_not_in_fore.index.tolist():
                table_data.drop(i, inplace=True)

        return table_data

    @staticmethod
    def get_table(table_name: str):
        """
        Trả về toàn bộ dữ liệu của bảng, nếu bảng không tồn tại sẽ bó lỗi.
        :return:
        """
        # Nếu bảng đã được đọc vào __AllTableData thì trả về dữ liệu của bảng,
        # #ngược lại lấy dữ lệu từ file
        table = TableControl.__AllTableData.get(table_name)
        if table is None:
            tb_fullname = table_name + '.csv'
            table = DataControl.read_table(tb_fullname)
            TableControl.__AllTableData.update({table_name: table})
        return TableControl.clean_data(table_name, table)

    # @staticmethod
    # def reload_data():
    #     keys = list(TableControl.__AllTableData.keys())
    #     TableControl.__AllTableData.clear()
    #     for key in keys:
    #         TableControl.get_table(key)

    @staticmethod
    def refresh_data():
        for key, value in TableControl.__AllTableData.items():
            TableControl.clean_data(key, value)

    @staticmethod
    def update(table_name: str, table: pd.DataFrame):
        table = TableControl.clean_data(table_name, table)
        DataControl.write_table(table_name + '.csv', table)
        TableControl.refresh_data()


if __name__ == '__main__':
    import random
    from datetime import time

    table = TableControl('ThoiKhoaBieu')
    khoaHocs = TableControl('KhoaHoc')
    makh_list = khoaHocs.table['MaKH'].tolist()
    days = ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy']
    time_list = [['7:00', '8:40'], ['8:50', '11:30'], ['7:00', '9:40'], ['13:00', '15:40'], ['13:00', '14:40'],
                 ['15:50', '17:30']]
    room_list = ['G6.201', 'G6.302', 'G7.101', 'G6.104', 'G6.101']
    for i in range(2000):
        id = table.get_new_id()
        makh = random.choice(makh_list)
        day = random.choice(days)
        c_time = random.choice(time_list)
        room = random.choice(room_list)
        d = {
            'MaTKB': id,
            'MaKH': makh,
            'Thu': day,
            'GioBD': c_time[0],
            'GioKT': c_time[1],
            'Phong': room
        }
        table.add(d)
    table.save_change()
