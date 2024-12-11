from flask import Flask, request, render_template
import sqlite3
import json

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('sales_data.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale REAL,
            expenses TEXT,
            savings REAL
        )
    ''')
    conn.close()

@app.route('/')
def form():
    return render_template('sales_form.html')

@app.route('/submit', methods=['POST'])
def submit_data():
    sale = float(request.form['sale'])
    expenses = [float(request.form.get(f'expense{i}', 0) or 0) for i in range(1, 11)]
    savings = float(request.form['savings'])

    # Store data in the database
    conn = sqlite3.connect('sales_data.db')
    conn.execute('INSERT INTO sales (sale, expenses, savings) VALUES (?, ?, ?)',
                 (sale, json.dumps(expenses), savings))
    conn.commit()
    conn.close()

    return "Data submitted successfully!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
