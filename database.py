import sqlite3 as sq

# with is used in order to control the entire section of databse

with sq.connect('sudoku_user_data.db') as con:
    cur = con.cursor()
    cur.execute(''' 
    
    CREATE TABLE IF NOT EXISTS users_data(

    username TEXT PRIMARY KEY,
    email TEXT,
    password TEXT,
    score INTEGER DEFAULT 0

    ) 
    
    ''')
