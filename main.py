import os
import sqlite3

from typing import List, Set


def execute_query(query_sql: str) -> List:
    '''
    Функция для выполнения запроса
    :param query_sql: запрос
    :return: результат выполнения запроса
    '''
    db_pass = os.path.join(os.getcwd(), 'chinook(1).db')
    connection = sqlite3.connect(db_pass)
    cur = connection.cursor()
    result = cur.execute(query_sql)
    return result


def unwrapper(records: List) -> None:
    '''
    Функция для вывода результата выполнения запроса
    :param records: список ответа БД
    '''
    for record in records:
        print(*record)


def get_employees() -> None:
    '''
    Функция получения всех записей из таблицы employees
    '''
    query_sql = '''
        SELECT *
          FROM employees;
    '''
    result = execute_query(query_sql)
    unwrapper(result)


# get_employees()

def get_filter_customers(state=None, city=None) -> None:
    query_sql = '''
    SELECT *
      FROM customers
    '''
    filter = ''
    if state and city:
        filter = f"WHERE State = '{state}' AND City = '{city}'"
    elif state:
        filter = f"WHERE State = '{state}'"
    elif city:
        filter = f"WHERE City = '{city}'"
    query_sql += filter
    result = execute_query(query_sql)
    unwrapper(result)


# get_filter_customers(state='SP', city='São Paulo')

def get_unique_customers() -> Set:
    query_sql = '''
        SELECT FirstName
          FROM customers
    '''
    names = list(execute_query(query_sql))
    unique_names = set()
    for name in names:
        unique_names.add(name[0])
    return len(unique_names)


result = get_unique_customers()


def get_unique_customers_by_sql() -> Set:
    query_sql = '''
        SELECT count(distinct FirstName)
          FROM customers
    '''
    unique_names_qty = list(execute_query(query_sql))[0][0]
    return unique_names_qty

def get_profit_by_sql() -> Set:
    query_sql = '''
        SELECT UnitPrice
          FROM invoice_items
    '''
    profit_qty = list(execute_query(query_sql))
    profit_qty_list = [*(x for t in profit_qty for x in t)]
    query_sql1 = '''  
        SELECT Quantity
          FROM invoice_items
    '''
    profit_qty_qual = list(execute_query(query_sql1))
    profit_qty_qual_list = [*(x for t in profit_qty_qual for x in t)]
    multiply_list = map(lambda x, y: x * y, profit_qty_qual_list, profit_qty_list)
    sum_uniprice = sum(multiply_list)


    return sum_uniprice


result = get_profit_by_sql()
print(result)

