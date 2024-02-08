import sqlite3
from langchain.tools import Tool

conn = sqlite3.connect('db.sqlite')

def run_sqlite_query(query):
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a query on the sqlite database",
    func=run_sqlite_query

)