from flask import Flask, jsonify
import sqlite3 as sq
app = Flask(__name__)



@app.route('/get_data', methods=['GET'])
def get_data():
    connect = sq.connect('2023.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM DaysOfWeekJanuary')
    data = cursor.fetchall()
    connect.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run()