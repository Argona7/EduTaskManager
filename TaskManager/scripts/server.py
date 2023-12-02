from flask import Flask, jsonify, request
import sqlite3 as sq
from DB import *
app = Flask(__name__)

update_functions = {
    'update_teachers_table' : update_teachers_table,
    'update_class_table' : update_class_table,
    'update_lessons_table' : update_lessons_table,
    'update_schedule_table' : update_schedule_table

}

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        date = request.args.get('date')
        table = request.args.get('table')
        connect = sq.connect(date[0])
        cursor = connect.cursor()
        if table == 'Schedule':
            cursor.execute(f'SELECT * FROM Schedule_{date[0]}_{date[1]}_{date[2]}')
        else:
            cursor.execute(f'SELECT * FROM {table}')
        data = cursor.fetchall()
        connect.close()
        return jsonify(data)

    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/update_data', methods=['POST'])
def update_data():
    try:
        data_request = request.get_json()

        year = data_request['year']
        function_update = data_request['function_update']
        data = data_request['data']
        delete = data_request['delete']

        connect = sq.connect(f'{year}.db')
        update_functions[function_update](connect, data, delete)
        connect.close()
        return 'Successful!'
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)