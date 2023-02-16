import sqlite3 as sql
from sqlite3 import Error


def connect(dbfile):
    '''create database connection'''
    con = None
    try:
        con = sql.connect(dbfile)
        print(sql.version)
    except Error as e:
        print(e)
    return con


def printout(cursor, table):
    '''prints the columns in the table'''
    cursor.execute(f'SELECT Name FROM {table}')
    columns = cursor.fetchall()
    [print(column) for column in columns]


def info(cursor, table):
    cursor.execute(f'PRAGMA table_info({table})')
    output = cursor.fetchall()
    print(type(output))
    print(output)


def dbview(cursor):
    '''lists all tables in database, and each column'''
    cursor.execute(r"SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        try:
            cursor.execute(f'SELECT * FROM {table[0]};')
            count = len(cursor.fetchall())
            print('{} (rows: {})'.format(table[0], count))
            cursor.execute(f'PRAGMA table_info({table[0]})')
            output = cursor.fetchall()
            for column in output:
                print('    {:4} -> {:20} {:20}'.format(*column))

        except:
            pass


def peek(table, cursor, n=10):
    '''prints out the first n rows of a table'''
    rows = cursor.execute(f'SELECT * FROM {table} LIMIT {n};')
    for row in rows:
        print(row)


def drop(table, cursor):
    '''drops the table from the database'''
    print(f'dropping table: {table}')
    cursor.execute(f'DROP TABLE {table};')


def deletempty(cursor):
    '''deletes any tables in the database with 0 rows'''
    # fetch all the tables
    cursor.execute(r"SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        tablename = table[0]
        try:
            # fetch all rows and count them
            cursor.execute(f'SELECT * FROM {tablename};')
            count = len(cursor.fetchall())
            # if the table is empty, delete it
            if count == 0:
                drop(tablename, cursor)
        except:
            pass

def deleteexcept(name, cursor):
    '''OMG NEVER USE THIS. drops all tables in a db except the named table'''
    # fetch all the tables
    cursor.execute(r"SELECT name FROM sqlite_master WHERE type='table';")
    for table in cursor.fetchall():
        tablename = table[0]
        try:
            # if the table is named boo, delete it
            if tablename != name:
                drop(tablename, cursor)
        except:
            pass




def binit(cursor):
    # cursor.execute(f'ALTER TABLE Fires ADD COLUMN xbin int16')
    # cursor.execute(f'ALTER TABLE Fires ADD COLUMN ybin int16')

    cursor.execute('SELECT OBJECTID, LATITUDE, LONGITUDE FROM Fires LIMIT 10;')
    print(cursor.fetchall())
    #for row in cursor.fetchall():
    #    cursor.execute(f'UPDATE Fires SET xbin = {round(row[2])}, ybin = {round(row[1])} WHERE OBJECTID = {row[0]}')


if __name__ == '__main__':
    db = connect(r'/home/snowdaere/PythonProjects/firecast/FireDatabase/FPA_FOD_20170508_LIVE.sqlite')
    cursor = db.cursor()
    # cursor.execute(f'ALTER TABLE Fires ADD COLUMN xbin int16')
    # cursor.execute(f'ALTER TABLE Fires ADD COLUMN ybin int16')

    #binit(cursor)

    deleteexcept('Fires', cursor)
    dbview(cursor)
    db.close()
