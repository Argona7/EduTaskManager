import sqlite3 as sq
from calendar import monthcalendar, monthrange
from argparse import ArgumentParser

# init helpful vars
# month = {
#     1: 'January',
#     2: 'February',
#     3: 'March',
#     4: 'April',
#     5: 'May',
#     6: 'June',
#     7: 'July',
#     8: 'August',
#     9: 'September',
#     10: 'October',
#     11: 'November',
#     12: 'December'
# }
#
# day = {
#     0: 'Понедельник',
#     1: 'Вторник',
#     2: 'Среда',
#     3: 'Четверг',
#     4: 'Пятница'
# }


# алгоритм расчёта рабочитх дней
# def count_working_days(year, month):
#     # getting calendar
#     cal = monthcalendar(year, month)
#     first_day, _ = monthrange(year, month)
#     # create counter for work days
#     working_days_count = 0
#     days_count = []
#
#     # run cycle week in month
#     for week in cal:
#         # run cycle day in week
#         for day in week:
#             # Добавляем только дни текущего месяца
#             # Добавляем только рабочие дни (пн-пт)
#             if day != 0 and (first_day + day - 1) % 7 < 5:
#                 working_days_count += 1
#                 days_count.append(day)
#
#     return (working_days_count, days_count)


def main():
    parser = ArgumentParser(description="Создание базы данных для указаннного года ")
    parser.add_argument('year', type=int, help='Год для создании базы данных')
    args = parser.parse_args()

    create_database(args.year)


# создание базы данных
def create_database(year):
    # connct to db
    db_name = f'{year}.db'
    with sq.connect(db_name) as connect:
        # create_month_table(connect)
        # create_days_table(connect, year)
        create_teachers_table(connect)
        create_classes_table(connect)
        create_lessons_table(connect)
        create_schedule_table(connect, ['2024','03','26'])
        return connect
    # close connect


# создание таблицы месяцев
# def create_month_table(connect):
#     quary_create_table = f'''
#     CREATE TABLE IF NOT EXISTS Months (
#     id INTEGER PRIMARY KEY,
#     month_name TEXT NOT NULL
#     )
#     '''
#     connect.cursor().execute(quary_create_table)
#     values = [(month[i],) for i in
#               range(1, 13)]  # массив values для заполнения таблицы Months поля month_name с помощью словаря month
#     quary_insert = f'''
#     INSERT INTO Months (month_name)
#     VALUES (?)
#     '''
#     connect.cursor().executemany(quary_insert, values)
#     connect.commit()


# создание и заполнение таблицы дней
# def create_days_table(connect, year):
#     for i in range(1, 13):
#         quary_create_table = f'''
#         CREATE TABLE IF NOT EXISTS DaysOfWeek{month[i]}(
#         id INTEGER PRIMARY KEY,
#         date TEXT NOT NULL,
#         name TEXT NOT NULL,
#         )
#         '''
#         connect.cursor().execute(quary_create_table)
#         count = monthrange(year, i)[0] if monthrange(year, i)[0] < 5 else 0  # получение первого рабочего дня месяца
#         len, date = count_working_days(year, i)
#         count_arr = [count]  # массив дней недели для execute_many
#         # заполнение дней в таблице дней
#         for j in range(len):
#             count = count + 1 if count < 4 else 0
#             count_arr.append(count)
#         values = [(i, date[j], day[count_arr[j]]) for j in range(len)]  # массив со всеми значениями
#         query_insert = f'''
#          INSERT INTO DaysofWeek{month[i]}(month_id, date,name)
#          VALUES (?,?,?)
#         '''
#         connect.cursor().executemany(query_insert, values)
#     connect.commit()


def create_teachers_table(connect):
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS Teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

def create_classes_table(connect):
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS Classes(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

def create_lessons_table(connect):
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS Lessons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id)  REFERENCES Teachers (id) ON UPDATE CASCADE ON DELETE CASCADE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

def create_schedule_table(connect, date: list):
    # создание расписания
    query_create_table = f'''
    CREATE TABLE IF NOT EXISTS Schedule_{date[0]}_{date[1]}_{date[2]}(
    id INTEGER PRIMARY KEY,
    day INTEGER,
    lesson_id INTEGER,
    class_id INTEGER ,
    lesson_time TEXT NOT NULL,
    FOREIGN KEY (lesson_id) REFERENCES Lessons (id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES Classes (id) ON UPDATE CASCADE ON DELETE CASCADE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

#data = {name : str}
def update_teachers_table(connect, data:dict, delete: bool):
    name = data['name']
    query_insert = '''
    INSERT INTO Teachers (name)
    VALUES (?)
    '''
    query_delete = '''
    DELETE FROM Teachers
    WHERE name = ?
    '''
    # проверка входных данных на тип массива
    if isinstance(name, list):
        # вставка или удаление данных
        name = [(i,) for i in name]
        if delete:
            connect.cursor().executemany(query_delete, name)
        else:
            connect.cursor().executemany(query_insert, name)
    # если элемент не имеет тип массива (строки, числа)
    else:
        # вставка или удаление данных
        if delete:
            connect.cursor().execute(query_delete, (name,))
        else:
            connect.cursor().execute(query_insert, (name,))
    connect.commit()

#data = {name: str}
def update_class_table(connect, data:dict, delete: bool):
    name = data['name']

    query_insert = '''
    INSERT INTO Classes(name)
    VALUES (?)
    '''
    query_delete = '''
    DELETE FROM Classes
    WHERE name = ?
    '''
    # проверка входных данных на тип массива
    if isinstance(name, list):
        # вставка или удаление данных
        name = [(i,) for i in name]
        if delete:
            connect.cursor().executemany(query_delete, name)
        else:
            connect.cursor().executemany(query_insert, name)
    # если элемент не имеет тип массива (строки, числа)
    else:
        # вставка или удаление данных
        if delete:
            connect.cursor().execute(query_delete, (name,))
        else:
            connect.cursor().execute(query_insert, (name,))
    connect.commit()



#data = {name : str, teacher_id : int}
def  update_lessons_table(connect, data:dict, delete: bool):
    name = data['name']
    teacher_id = data['teacher_id']

    query_insert = '''
    INSERT INTO Lessons(name, teacher_id)
    VALUES (?,?)
    '''
    query_delete = '''
    DELETE FROM Lessons
    WHERE name = ?
    '''
    # проверка входных данных на тип массива
    if all(isinstance(arg, list) for arg in [name, teacher_id]):
        # вставка или удаление данных
        values = [(i, j) for i, j in zip(name, teacher_id)]
        if delete:
            name = [(i,) for i in name]
            connect.cursor().executemany(query_delete, name)
        else:
            connect.cursor().executemany(query_insert, values)
    # проверка входных данных на тип массива , (если 1 условие неверно , но верно 2 условие то вызывается ошибка несоответствия типов)
    elif any(isinstance(arg, list) for arg in [name, teacher_id]):
        raise TypeError
    # если элементы не имеют тип массива (строки, числа)
    else:
        # вставка или удаление данных
        if delete:
            connect.cursor().execute(query_delete, (name,))
        else:
            connect.cursor().execute(query_insert, (name, teacher_id))
    connect.commit()


#data = {date:list ,id:int, day:int , lesson_id: int, class_id : int}
def update_schedule_table(connect, data:dict, delete: bool, ):
    date = data['date']
    id = data['id']
    day = data['day']
    lesson_id = data['lesson_id']
    class_id = data['class_id']
    lesson_time = data['lesson_time']
    query_insert = f'''
    INSERT INTO Schedule_{date[0]}_{date[1]}_{date[2]}(day, lesson_id, class_id, lesson_time)
    VALUES (?,?,?,?)
    '''
    query_delete = f'''
    DELETE FROM Schedule_{date[0]}_{date[1]}_{date[2]}
    WHERE id = ?
    '''
    # проверка входных данных на тип массива
    if all(isinstance(arg, list) for arg in [day, lesson_id, class_id, lesson_time]):
        values = [(i, j, k, l) for i, j, k, l in zip(day, lesson_id, class_id, lesson_time)]
        # вставка или удаление данных
        if delete:
            Day = [(i,) for i in id]
            connect.cursor().executemany(query_delete, Day)
        else:
            connect.cursor().executemany(query_insert, values)
    # проверка входных данных на тип массива , (если 1 условие неверно , но верно 2 условие то вызывается ошибка несоответствия типов)
    elif any(isinstance(arg, list) for arg in [day, lesson_id, class_id, lesson_time]):
        raise TypeError
    # если элементы не имеют тип массива (строки, числа)
    else:
        # вставка или удаление данных
        if delete:
            connect.cursor().execute(query_delete, (id,))
        else:
            connect.cursor().execute(query_insert, (day, lesson_id, class_id, lesson_time))

    connect.commit()

if __name__ == '__main__':
    main()
