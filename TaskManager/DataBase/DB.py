import sqlite3 as sq
from calendar import monthcalendar,monthrange
from time import time

# init helpful vars
month = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

day = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday'
}


#алгоритм расчёта рабочитх дней
def count_working_days(year, month):
    # getting calendar
    cal = monthcalendar(year, month)
    first_day, _ = monthrange(year, month)
    # create counter for work days
    working_days_count = 0
    days_count = []

    # run cycle week in month
    for week in cal:
        # run cycle day in week
        for day in week:
            # Добавляем только дни текущего месяца
            # Добавляем только рабочие дни (пн-пт)
            if day != 0 and (first_day + day - 1) % 7 < 5:
                working_days_count += 1
                days_count.append(day)

    return (working_days_count, days_count)


# создание базы данных
def create_database(year):
    # connect to db
    db_name  = f'{year}.db'
    with sq.connect(db_name) as connect:
        create_month_table(connect)
        create_days_table(connect, year)
        create_teachers_table(connect)
        create_classes_table(connect)
        create_lessons_table(connect)
        create_schedule_table(connect)
    # close connect



# создание таблицы месяцев
def create_month_table(connect):
    quary_create_table= f'''
    CREATE TABLE IF NOT EXISTS Months (
    id INTEGER PRIMARY KEY,
    month_name TEXT NOT NULL
    ) 
    '''
    connect.cursor().execute(quary_create_table)
    values = [(month[i],) for i in range(1,13)] #массив values для заполнения таблицы Months поля month_name с помощью словаря month
    quary_insert = f'''
    INSERT INTO Months (month_name)
    VALUES (?)
    '''
    connect.cursor().executemany(quary_insert, values)
    connect.commit()


# создание и заполнение таблицы дней
def create_days_table (connect, year):
    for i in range(1,13):
        quary_create_table = f'''
        CREATE TABLE IF NOT EXISTS DaysOfWeek{month[i]}(
        id INTEGER PRIMARY KEY,
        month_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (month_id) REFERENCES Months(id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        '''
        connect.cursor().execute(quary_create_table)
        count = monthrange(year,i)[0] if monthrange(year,i)[0] < 5 else 0 #получение первого рабочего дня месяца
        len, date = count_working_days(year, i)
        count_arr = [count] # массив дней недели для execute_many
        #заполнение дней в таблице дней
        for j in range(len):
            count = count + 1 if count < 4 else 0
            count_arr.append(count)
        values = [(i,date[j],day[count_arr[j]]) for j in range(len)]  #массив со всеми значениями
        query_insert = f'''
         INSERT INTO DaysofWeek{month[i]}(month_id, date,name)
         VALUES (?,?,?)
        '''
        connect.cursor().executemany(query_insert, values)
    connect.commit()


def create_teachers_table(connect):
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS Teachers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

def edit_teachers_table(connect, data, delete):
    query_insert = '''
    INSERT INTO Teachers (name)
    VALUES (?)
    '''
    query_delete = '''
    DELETE FROM Teachers
    WHERE name = ?
    '''

    if type(data) == str:
        data = (data,)
        if delete:
            connect.cursor().execute(query_delete, data)
        else:
            connect.cursor().execute(query_insert, data)
    else:
        data = [(i,) for i in data]
        if delete:
            connect.cursor().executemany(query_delete, data)
        else:
            connect.cursor().executemany(query_insert, data)
    connect.commit()


def create_classes_table (connect):
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS Classes(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

def edit_class_table (connect , data , delete):
    query_insert = '''
    INSERT INTO Classes(name)
    VALUES (?)
    '''
    query_delete = '''
    DELETE FROM Classes
    WHERE name = ?
    '''

    if type(data) == str:
        data = (data,)
        if delete:
            connect.cursor().execute(query_delete, data)
        else:
            connect.cursor().execute(query_insert, data)
    else:
        data = [(i,) for i in data]
        if delete:
            connect.cursor().executemany(query_delete, data)
        else:
            connect.cursor().executemany(query_insert, data)
    connect.commit()

def create_lessons_table(connect):
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS Lessons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
    )
    '''
    connect.cursor().execute(query_create_table)
    connect.commit()

def edit_lessons_table (connect, data, delete):
    query_insert = '''
    INSERT INTO Lessons(name)
    VALUES (?)
    '''
    query_delete = '''
    DELETE FROM Lessons
    WHERE name = ?
    '''

    if type(data) == str:
        data = (data,)
        if delete:
            connect.cursor().execute(query_delete, data)
        else:
            connect.cursor().execute(query_insert, data)
    else:
        data = [(i,) for i in data]
        if delete:
            connect.cursor().executemany(query_delete, data)
        else:
            connect.cursor().executemany(query_insert, data)
    connect.commit()

def create_schedule_table(connect):
    for i in range(1,13):
        query_create_table = f'''
        CREATE TABLE IF NOT EXISTS Schedule{month[i]} (
        id INTEGER PRIMARY KEY,
        day_id INTEGER,
        lesson_id INTEGER,
        teacher_id INTEGER,
        class_id INTEGER,
        FOREIGN KEY (day_id) REFERENCES DaysOfWeek{month[i]}(id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (lesson_id) REFERENCES Lessons (id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (teacher_id)  REFERENCES Teachers (id) ON UPDATE CASCADE ON DELETE CASCADE,
        FOREIGN KEY (class_id) REFERENCES Classes (id) ON UPDATE CASCADE ON DELETE CASCADE
        )
        '''
        connect.cursor().execute(query_create_table)
    connect.commit()

def edit_schedule_table (commit , data , delete):
    pass








if __name__ == "__main__":
    start = time()
    create_database(2023)
    end = time()
    print(end-start)
