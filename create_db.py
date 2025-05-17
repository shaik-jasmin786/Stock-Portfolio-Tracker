import sqlite3

conn = sqlite3.connect('portfolio.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS stocks (
        symbol TEXT,
        quantity INTEGER,
        buy_price REAL
    )
''')
conn.commit()
conn.close()

print("Database created successfully!")