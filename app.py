#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
produkt = []
try:
    with open('./data.json', 'r') as f:
        produkt = json.load(f)
except:
    produkt = []


@app.route('/', methods=['GET', 'POST'])
def index():
    edit_id = request.args.get('edit')
    if request.method == "GET":

        
        if edit_id is not None:
            produkt_value = produkt[int(edit_id)][0]
            ilosc_value = produkt[int(edit_id)][1]
            form_action = url_for('index', edit=edit_id)
        else:
            produkt_value = ''
            ilosc_value = ''
            form_action = url_for('index')

        
        return render_template("index.html", produkt=produkt, produkt_value=produkt_value, ilosc_value=ilosc_value, form_action=form_action)
    
    else:
        if edit_id is not None:
            produkt[int(edit_id)] = (request.form['produkt'], request.form['ilosc'])
        else:
            produkt.append((request.form["produkt"], request.form["ilosc"]))
        
        with open('./data.json', 'w') as f:
            json.dump(produkt, f)

        return redirect(url_for('index'))

@app.route("/usun/<int:id>")
def usun(id):
    produkt.pop(id)
    with open('./data.json', 'w') as f:
            json.dump(produkt, f)
    return redirect(url_for('index'))

    

@app.route('/about')
def about():
    return 'we are programmers'

if __name__ == '__main__':
    app.run(debug=True)