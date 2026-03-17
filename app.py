#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
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

        tabela = f'''<tr>
    <th>Produkt</th>
    <th>Ilość</th>
    <th>Usuń</th>
    <th>Edytuj</th>
  </tr>'''
        for index, (produkty, ilosc) in enumerate(produkt):
            tabela += f'''<tr>
            <td>{produkty}</td>
            <td>{ilosc}</td>
            <td><a href="{url_for('usun', id=index)}">Usuń</a></td>
            <td><a href="{url_for('index', edit=index)}">Edytuj</a></td>
        </tr>'''
        
        body = f'''
        <link rel="stylesheet" href="{url_for("static", filename="style.css")}">
<form id="zakupy" action="{form_action}" method="POST">
    <h1>Lista zakupów</h1><br>
    <label for="produkt">Produkt</label>
    <input type="text" id="produkt" name="produkt" value='{produkt_value}'><br>
    <label for="ilosc">Ilość</label>
    <input type="text" id="ilosc" name="ilosc" value='{ilosc_value}'>
    <input type="submit" value="send"></form>
    <table>
    {tabela}</table>

'''
        return body
    
    else:
        if edit_id is not None:
            produkt[int(edit_id)] = (request.form['produkt'], request.form['ilosc'])
        else:
            produkt.append((request.form["produkt"], request.form["ilosc"]))
        

        return redirect(url_for('index'))

@app.route("/usun/<int:id>")
def usun(id):
    produkt.pop(id)
    return redirect(url_for('index'))
"""
@app.route("/edytuj/<int:id>", methods=['GET', 'POST'])
def edytuj(id):
    if request.method == "GET":
        body = f'''
<form id="zakupy" action="{url_for('edytuj', id=id)}" method='POST'>
<h1>Lista zakupów</h1><br>
    <label for="produkt">Produkt</label>
    <input type="text" id="produkt" name="produkt" value='{produkt[id][0]}'><br>
    <label for="ilosc">Ilość</label>
    <input type="text" id="ilosc" name="ilosc" value='{produkt[id][1]}'>
    <input type="submit" value="send">
    <table></table></form>
    '''
    
        return body
    
    else:
        produkt[id] = (request.form["produkt"], request.form["ilosc"])
        return redirect(url_for('index'))
"""
    

@app.route('/about')
def about():
    return 'we are programmers'

if __name__ == '__main__':
    app.run(debug=True)