import sqlite3 
import pandas as pd


# Подключаемся к базе данных
conn = sqlite3.connect('/projects/final_bot/finances.db')
c = conn.cursor()

# Функция проверяем наличие таблицы пользователи и если нет - создает ее
def create_table(name):
    sql_query = (
    f'''
    CREATE TABLE IF NOT EXISTS {name} (
    "index" INTEGER NOT NULL,
    date DATE,
    income FLOAT,
    expend FLOAT,
    description VARCHAR(100),
    bank VARCHAR(20)
    );
    '''
    )
    c.execute(sql_query)


# Функция считает количество записей в базе данных
def find_count(name):
    sql_query = f'SELECT COUNT(*) FROM {name};'
    return c.execute(sql_query).fetchone()[0]


# Функция выгрузки всех записей из базы данных и перевод в csv
def get_budget(name):
    sql_query = f'SELECT * FROM {name};'
    df = pd.read_sql(sql_query, con=conn)
    df = df.drop(columns='index')
    df.to_csv('/projects/final_bot/files/all_data.csv')


# Функция добавления записей в базу данных
def add_operation(name, is_now, income, expend, bank):
    sql_query = (
    '''INSERT INTO {} ("index", date, income, expend, description, bank)
    VALUES ({}, {}, {}, {}, 'test', '{}')'''
    .format(name, find_count(name), is_now, income, expend, bank)
    )
    c.execute(sql_query)
    conn.commit()
