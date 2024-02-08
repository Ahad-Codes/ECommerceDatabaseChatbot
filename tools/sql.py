import sqlite3
from langchain.tools import Tool
from pydantic import BaseModel
from typing import List

conn = sqlite3.connect('db.sqlite')

def list_tables():
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join([row[0] for row in rows if rows[0] is not None])  

def run_sqlite_query(query):

    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occurred : {str(err)}"


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a query on the sqlite database",
    func=run_sqlite_query

)

def describe_tables(tables_name):
    c = conn.cursor()
    tables = ', '.join("'" + table + "'" for table in tables_name.split(','))
    rows = c.execute(f'SELECT sql from sqlite_master where type="table" and name in ({tables})')
    return '\n'.join(row[0] for row in rows if row[0] is not None)



describe_tables_tool = Tool.from_function(
    name = "describe_tables",
    description= "Given a list of table names, return the schema of the tables",
    func= describe_tables
)