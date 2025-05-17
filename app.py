import os
print("creating DB in:",os.getcwd())
from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stocks (
                 symbol TEXT, quantity INTEGER, buy_price REAL)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stocks")
    rows = c.fetchall()
    conn.close()

    portfolio_data = []
    total_value = 0

    for symbol, qty, buy_price in rows:
        stock = yf.Ticker(symbol)
        try:
            current_price = stock.info['regularMarketPrice']
        except:
            current_price = 0

        current_value = qty * current_price
        gain_loss = (current_price - buy_price) * qty
        total_value += current_value

        portfolio_data.append({
            'symbol': symbol,
            'quantity': qty,
            'buy_price': buy_price,
            'current_price': round(current_price, 2),
            'current_value': round(current_value, 2),
            'gain_loss': round(gain_loss, 2)
        })

    return render_template('portfolio.html', stocks=portfolio_data, total=round(total_value, 2))

@app.route('/add', methods=['POST'])
def add_stock():
    symbol = request.form['symbol'].upper()
    quantity = int(request.form['quantity'])
    buy_price = float(request.form['buy_price'])

    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("INSERT INTO stocks VALUES (?, ?, ?)", (symbol, quantity, buy_price))
    conn.commit()
    conn.close()
    return redirect('/portfolio')

@app.route('/delete/<symbol>')
def delete_stock(symbol):
    conn = sqlite3.connect('portfolio.db')
    c = conn.cursor()
    c.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
    conn.commit()
    conn.close()
    return redirect('/portfolio')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)