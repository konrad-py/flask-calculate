#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
produkt = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        body = f'''
<form id="zakupy", action="{url_for('index')}", method="POST">
    <h1>Lista zakupów</h1><br>
    <label for="produkt">Produkt</label>
    <input type="text", id="produkt", name="produkt"><br>
    <label for="ilosc">Ilość</label>
    <input type="text", id="ilosc", name="ilosc">
    <input type="submit", value="send">
    <h2>{produkt}

'''
        return body
    
    else:
        produkt.append((request.form["produkt"], request.form["ilosc"]))

        return redirect(url_for('index'))



@app.route('/about')
def about():
    return 'we are programmers'

if __name__ == '__main__':
    app.run(debug=True)