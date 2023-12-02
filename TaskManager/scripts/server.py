from flask import Flask, jsonify, request
import sqlite3 as sq
from DB import *

app = Flask(__name__)

#update функции таблиц базы данных
update_functions = {
    'update_teachers_table' : update_teachers_table,
    'update_class_table' : update_class_table,
    'update_lessons_table' : update_lessons_table,
    'update_schedule_table' : update_schedule_table

}

#Функция для получения данных приложения из базы данных
@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        #получение данных из параметров get запроса
        date = request.args.getlist('date')
        table = request.args.get('table')
        #подключение к базе данных
        connect = sq.connect(f'{date[0]}.db')
        cursor = connect.cursor()
        #выборка данных изходя ищ параметров
        if table == 'Schedule':
            cursor.execute(f'SELECT * FROM Schedule_{date[0]}_{date[1]}_{date[2]}')
        else:
            cursor.execute(f'SELECT * FROM {table}')
        data = cursor.fetchall()
        connect.close()
        #возвращение данных в json формате
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': 'Bad Request', 'details': {'error': str(e)}})

#функция для изменения данных базы данных приложением
@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        data_request = request.get_json()
        #записывание данных из json
        year = data_request['year']
        function_update = data_request['function_update']
        data = data_request['data']
        delete = bool(data_request['delete'])
        #подключение к базе данных
        connect = sq.connect(f'{year}.db')
        #изменение данных в таблице
        update_functions[function_update](connect, data, delete)
        connect.close()
        return 'Data updated successfully'
    except Exception as e:
        return jsonify({'error': 'Bad Request', 'details' : {'error' : str(e)}})

if __name__ == "__main__":
    #запуск сервера
    app.run(debug=False)