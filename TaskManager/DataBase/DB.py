import sqlite3 as sq
from calendar import monthcalendar, weekday
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
    # create counter for work days
    working_days_count = 0

    # run cycle week in month
    for week in cal:
        # run cycle day in week
        for day in week:
            # Добавляем только дни текущего месяца
            if day != 0:
                # Добавляем только рабочие дни (пн-пт)
                if weekday(year, month, day) < 5:
                    working_days_count += 1

    return working_days_count


# создание базы данных
def create_database(year):
    # connect to db
    connect = sq.connect(f'{year}.db')
    create_month_table(connect)
    create_days_table(connect, year)
    # close connect
    connect.close()


# создание таблицы месяцев
def create_month_table(connect):

    for i in range (1,13):
        quary_create_table= f'''
        CREATE TABLE IF NOT EXISTS {month[i]} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_name TEXT NOT NULL
        ) 
        '''
        connect.cursor().execute(quary_create_table)
        quary_insert = f'''
        INSERT INTO {month[i]} (month_name)
        VALUES (?)
        '''
        connect.cursor().execute(quary_insert, (month[i],))
        connect.commit()


# создание и заполнение таблицы дней
def create_days_table (connect, year):
    for i in range(1,13):
        quary_create_table = f'''
        CREATE TABLE IF NOT EXISTS DaysOfWeek{month[i]}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (month_id) REFERENCES {month[i]}(id)
        )
        '''
        connect.cursor().execute(quary_create_table)
        count = 0
        #получение первого рабочего дня месяца
        #заполнение дней в таблице дней
        for _ in range(count_working_days(year, i)):

            query_insert = f'''
            INSERT INTO DaysofWeek{month[i]}(month_id, name)
            VALUES (?,?)
           '''
            connect.cursor().execute(query_insert, (i,day[count],))
            count = count + 1 if count < 4 else 0
        connect.commit()


if __name__ == "__main__":
    start = time()
    create_database(2023)
    end = time()
    print(f"\n\n[*] Speed test ILO\nFunc > create_database()\nArgs > 2023: int\nResult > {end-start}")