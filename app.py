#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "zakupy.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS produkty (id INTEGER PRIMARY KEY AUTOINCREMENT, produkt TEXT NOT NULL,ilosc TEXT NOT NULL)')
    db.commit()

with app.app_context():
    init_db()


@app.route('/', methods=['GET', 'POST'])
def index():

    edit_id = request.args.get('edit')
    if request.method == "GET":

        db = get_db()

        cursor = db.execute('SELECT id, produkt, ilosc FROM produkty')
        produkty = cursor.fetchall()
        
        if edit_id is not None:
            cursor = db.execute('SELECT id, produkt, ilosc FROM produkty WHERE id = ?', (edit_id,))
            prod = cursor.fetchone()
            produkt_value = prod['produkt']
            ilosc_value = prod['ilosc']
            form_action = url_for('index', edit=edit_id)
        else:
            produkt_value = ''
            ilosc_value = ''
            form_action = url_for('index')

        
        return render_template("index.html", produkty=produkty, produkt_value=produkt_value, ilosc_value=ilosc_value, form_action=form_action)
    
    else:
        db = get_db()
        if edit_id is not None:
            db.execute('UPDATE produkty SET produkt = ?, ilosc = ? WHERE id = ?', (request.form['produkt'], request.form['ilosc'], edit_id))
            db.commit()
        else:
            db.execute('INSERT INTO produkty (produkt, ilosc) VALUES (?, ?)', (request.form['produkt'], request.form['ilosc']))
            db.commit()
        
        

        return redirect(url_for('index'))

@app.route("/usun/<int:id>")
def usun(id):
    db = get_db()
    db.execute('DELETE FROM produkty WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))

    

@app.route('/about')
def about():
    return 'we are programmers'

if __name__ == '__main__':
    app.run(debug=True)