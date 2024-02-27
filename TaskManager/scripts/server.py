from flask import Flask, jsonify, request
import sqlite3 as sq
from DB import *

app = Flask(__name__)

# update функции таблиц базы данных
update_functions = {
    'update_teachers_table': update_teachers_table,
    'update_class_table': update_class_table,
    'update_lessons_table': update_lessons_table,
    'update_schedule_table': update_schedule_table

}


def get_last_day(date):
    months_days = {'01': '31', '02': '28', '03': '31', '04': '30', '05': '31',
                   '06': '30', '07': '31', '08': '31', '09': '30', '10': '31',
                   '11': '30', '12': '31'}

    if int(date[0]) % 4 == 0:
        months_days['02'] = '29'
    if date[1] == '01':
        last_month = '12'
    else:
        last_month = f'0{int(date[1][-1]) - 1}'
    return months_days[last_month]


def get_cards(data):
    cards = list()
    for lesson in data:
        card = {'LessonName': lesson[1], 'TeacherName': lesson[2], 'ClassName': lesson[3], 'LessonTime': lesson[4]}
        cards.append(card)

    return cards


# Функция для получения данных приложения из базы данных
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # получение данных из параметров get запроса
        date = request.args.getlist('date')
        table = request.args.get('table')
        # подключение к базе данных
        connect = sq.connect(f'{date[0]}.db')
        cursor = connect.cursor()
        # выборка данных изходя ищ параметров
        if table == 'Schedule':
            schedule_table_name = f"Schedule_{date[0]}_{date[1]}_{date[2]}"
            get_schedule_query = f"""
            SELECT day, Lessons.name, Teachers.name, Classes.name, lesson_time
            FROM {schedule_table_name}
            INNER JOIN Lessons ON {schedule_table_name}.lesson_id = Lessons.id
            INNER JOIN Teachers ON Lessons.teacher_id = Teachers.id
            INNER JOIN Classes ON {schedule_table_name}.class_id = Classes.id
            """
            cursor.execute(get_schedule_query)
        else:
            cursor.execute(f'SELECT * FROM {table}')
        data = cursor.fetchall()
        connect.close()
        data_json = {'MonthInfo':
                         {'LastMonthDays': get_last_day(date),
                          'NowMonthDays': date[1],
                          'SliceDay': data[0][0]
                          },
                     'HomeWork': {
                         'Cards': get_cards(data)
                     }
                     }
        # возвращение данных в json формате
        return f"{data_json}"

    except Exception as e:
        return jsonify({'error': 'Bad Request', 'details': {'error': str(e)}})


# функция для изменения данных базы данных приложением
@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        data_request = request.get_json()
        # записывание данных из json
        year = data_request['year']
        function_update = data_request['function_update']
        data = data_request['data']
        delete = bool(data_request['delete'])
        # подключение к базе данных
        connect = sq.connect(f'{year}.db')
        # изменение данных в таблице
        update_functions[function_update](connect, data, delete)
        connect.close()
        return 'Data updated successfully'
    except Exception as e:
        return jsonify({'error': 'Bad Request', 'details': {'error': str(e)}})


if __name__ == "__main__":
    # запуск сервера
    app.run(debug=False, ssl_context=('../cert/certificate.crt', '../cert/privateKey.key'))
