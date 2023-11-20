import sqlite3 as sq
import calendar
month = {1: 'January',
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
         12: 'December'}

day = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday'
}

def count_working_days(year, month):
    cal = calendar.monthcalendar(year, month)
    working_days = sum(1 for week in cal for day in week if day != 0 and day < 6)
    return working_days
def create_database(year):
    connect = sq.connect(f'{year}.db')
    create_month_table(connect)
    create_days_table(connect, year)
    connect.close()


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
        for j in range(1, count_working_days(year, i) + 1):
            query_insert = f'''
            INSERT INTO DaysofWeek{month[i]}(month_id, name)
            VALUES (?,?)
           '''
            connect.cursor().execute(query_insert, (i,))

        connect.commit()

create_database(2023)






