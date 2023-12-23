import json
import os
from datetime import time

package_path = os.path.dirname(__file__)
file_path = os.path.join(package_path, 'customdata.json')


class CustomData:

    @staticmethod
    def write_data(data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    @staticmethod
    def load_data():
        """
        Đọc và tả về toàn ộ dữ liệu được lưu trong file 'customdata.json'
        :return:
        """

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_room(room: str):
        if room not in CustomData.Rooms:
            data = CustomData.load_data()
            CustomData.Rooms.append(room)
            data['room'] = CustomData.Rooms
            CustomData.write_data(data)

    @staticmethod
    def normalize_time(hour, time):
        hour += time // 60
        time = time % 60
        return hour, time

    @staticmethod
    def generate_timetable():
        curTime = time(7, 0)
        for i in range(1, 14):
            if i in [3, 4, 8, 9, 13]:
                curTime = curTime.replace(*CustomData.normalize_time(curTime.hour, curTime.minute + 10))
            if i == 6:
                curTime = time(13, 0)
            elif i == 11:
                curTime = time(18, 30)
            start = curTime
            curTime = curTime.replace(*CustomData.normalize_time(curTime.hour, curTime.minute + 50))
            # print(f'{i}: [time({start.hour},{start.minute}), time({curTime.hour},{curTime.minute})],')
            print(f'"{i}": ["{start.strftime("%H:%M")}", "{curTime.strftime("%H:%M")}"],')

    @staticmethod
    def lesson_range():
        return list(CustomData.Lessons.keys())

    @staticmethod
    def lesson_to_time(lesson: str):
        return CustomData.Lessons.get(lesson)

    @staticmethod
    def find_lesson_by_time(start_time: str, end_time: str):
        lessons = []
        find_start_time = True
        for lesson, time_list in CustomData.Lessons.items():
            # Tìm thòi gian đầu khớp
            if find_start_time:
                l_time = time(*map(int, time_list[0].split(":")))
                in_time = time(*map(int, start_time.split(':')))
                if in_time == l_time:
                    find_start_time = False
            # Tìm thời gian kết thúc khớp
            if not find_start_time:
                l_time = time(*map(int, time_list[1].split(":")))
                in_time = time(*map(int, end_time.split(':')))
                if in_time == l_time:
                    lessons.append(lesson)
                    return lessons
                else:
                    lessons.append(lesson)
        return None

    @staticmethod
    def get_day(id: str):
        return CustomData.Days.get(id)

    @staticmethod
    def time_format(start_time: str, end_time: str):
        time = CustomData.find_lesson_by_time(start_time, end_time)
        if time is not None:
            return ', '.join(time)
        else:
            return f"{start_time} -> {end_time}"

    @staticmethod
    def get_id_Thu(Thu:str):
        d = {
            'thứ hai': 2,
            'thứ ba': 3,
            'thứ tư': 4,
            'thứ năm': 5,
            'thứ sáu': 6,
            'thứ bảy': 7,
            'chủ nhật': 8
        }
        return d.get(Thu.lower())


    Lessons: dict = load_data().get('lesson')
    Days: dict = load_data().get('day')
    Rooms: list = load_data().get('room')
    Semesters:list = load_data().get('semester')


if __name__ == '__main__':
    print(CustomData.find_lesson_by_time("7:00", "13:50"))
