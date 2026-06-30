#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3, os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "zakupy.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

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
    db.execute('CREATE TABLE IF NOT EXISTS produkty (id INTEGER PRIMARY KEY AUTOINCREMENT, produkt TEXT NOT NULL, ilosc TEXT NOT NULL, data_dodania TEXT, sklep TEXT)')
    db.execute('CREATE TABLE IF NOT EXISTS budowa (id INTEGER PRIMARY KEY AUTOINCREMENT, produkt TEXT NOT NULL, koszt TEXT NOT NULL, ilosc TEXT NOT NULL, sklep TEXT, data TEXT NOT NULL)')
    
    db.commit()

with app.app_context():
    init_db()


@app.route('/', methods=['GET', 'POST'])
def index():

    user = session.get('user')
    if user is None:
        return redirect(url_for("login"))
    
    edit_id = request.args.get('edit')
    if request.method == "GET":

        db = get_db()

        cursor = db.execute('SELECT id, produkt, ilosc, data_dodania, sklep FROM produkty')
        produkty = cursor.fetchall()
        
        if edit_id is not None:
            cursor = db.execute('SELECT id, produkt, ilosc, sklep FROM produkty WHERE id = ?', (edit_id,))
            prod = cursor.fetchone()
            if prod:
                produkt_value = prod['produkt']
                ilosc_value = prod['ilosc']
                sklep_value = prod['sklep']
                form_action = url_for('index', edit=edit_id)
            else:
                return redirect(url_for('index'))
        else:
            produkt_value = ''
            ilosc_value = ''
            sklep_value = ''
            form_action = url_for('index')

        
        return render_template("index.html", produkty=produkty, produkt_value=produkt_value, ilosc_value=ilosc_value, form_action=form_action, sklep_value=sklep_value)
    
    else:
        db = get_db()
        if edit_id is not None:
            db.execute('UPDATE produkty SET produkt = ?, ilosc = ?, sklep = ? WHERE id = ?', (request.form['produkt'], request.form['ilosc'], request.form['sklep'], edit_id))
            db.commit()
        else:
            data_dodania = datetime.today().strftime('%Y-%m-%d')
            db.execute('INSERT INTO produkty (produkt, ilosc, data_dodania, sklep) VALUES (?, ?, ?, ?)', (request.form['produkt'], request.form['ilosc'], data_dodania, request.form['sklep']))
            db.commit()
        
        return redirect(url_for('index'))

@app.route("/usun/<int:id>")
def usun(id):
    user = session.get('user')
    if user is None:
        return redirect(url_for("login"))
    
    db = get_db()
    db.execute('DELETE FROM produkty WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))

######<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<LOGIN>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if ((user == os.getenv('SHOP_USER_1') and password == os.getenv('SHOP_PASS_1')) 
            or (user == os.getenv('SHOP_USER_2') and password == os.getenv('SHOP_PASS_2'))
        ):
            session['user'] = user
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="wrong username or password")
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


######<<<<<<<<<<<<<<BUDOWA>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@app.route("/budowa_usun/<int:id>")
def budowa_usun(id):
    user = session.get('user')
    if user is None:
        return redirect(url_for("login"))
    
    db = get_db()
    db.execute('DELETE FROM budowa WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('budowa'))


@app.route("/budowa", methods=['GET', 'POST'])
def budowa():
    user = session.get('user')
    if user is None:
        return redirect(url_for("login"))
    
    edit_id = request.args.get('edit')
    if request.method == "GET":

        db = get_db()

        cursor = db.execute('SELECT id, produkt, koszt, ilosc, data, sklep FROM budowa')
        budowa_items = cursor.fetchall()
        
        suma = 0
        for item in budowa_items:
            cena = float(item['koszt'])
            suma += cena

        error = None

        if edit_id is not None:
            cursor = db.execute('SELECT id, produkt, koszt, ilosc, sklep FROM budowa WHERE id = ?', (edit_id,))
            prod = cursor.fetchone()
            if prod:
                produkt_value = prod['produkt']
                koszt_value = prod['koszt']
                ilosc_value = prod['ilosc']
                sklep_value = prod['sklep']
                form_action = url_for('budowa', edit=edit_id)
            else:
                return redirect(url_for('budowa'))
        else:
            produkt_value = ''
            koszt_value = ''
            ilosc_value = ''
            sklep_value = ''
            form_action = url_for('budowa')

        
        return render_template("budowa.html", budowa_items=budowa_items, produkt_value=produkt_value, koszt_value=koszt_value, ilosc_value=ilosc_value, form_action=form_action, sklep_value=sklep_value, error=error, suma=suma)
    
    else:
        db = get_db()
        try:
            koszt = float(request.form['koszt'].replace(',', '.'))

            if edit_id is not None:
                db.execute('UPDATE budowa SET produkt = ?, koszt = ?, ilosc = ?, sklep = ? WHERE id = ?', (request.form['produkt'], koszt, request.form['ilosc'], request.form['sklep'], edit_id))
                db.commit()
            else:
                data = datetime.today().strftime('%Y-%m-%d')
                db.execute('INSERT INTO budowa (produkt, koszt, ilosc, data, sklep) VALUES (?, ?, ?, ?, ?)', (request.form['produkt'], koszt, request.form['ilosc'], data, request.form['sklep']))
                db.commit()
            
            return redirect(url_for('budowa'))
        
        except:
            error = "W polu koszt można wpisać tylko liczbę"
            cursor = db.execute('SELECT id, produkt, koszt, ilosc, data, sklep FROM budowa')
            budowa_items = cursor.fetchall()
            suma = 0
            for item in budowa_items:
                cena = float(item['koszt'])
                suma += cena
            return render_template('budowa.html', produkt_value=request.form['produkt'], koszt_value=request.form['koszt'], ilosc_value=request.form['ilosc'], sklep_value=request.form['sklep'], error=error, budowa_items=budowa_items, suma=suma)


@app.route('/about')
def about():
    user = session.get('user')
    if user is None:
        return redirect(url_for("login"))
    return 'we are programmers'

if __name__ == '__main__':
    app.run()