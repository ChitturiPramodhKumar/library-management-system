from flask import Flask, render_template, redirect, url_for, request
from db.libms_ops import inventory_handler
import json_data
from datetime import datetime
from db.globals import *

app = Flask('__name__')


# app.jinja_env.filters['zip'] = zip

@app.route('/')
def welcomepage():
    return render_template('welcomepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

#returns data in json format
@app.route('/allbooks')
def books():
    data = inventory_handler.get_allbooks(INVENTORY_TABLE,result_dict= True)
    return data

@app.route('/showallbooks')
def render_all_book():
    # data = json_data.get_inventory_data()
    data = inventory_handler.get_allbooks(INVENTORY_TABLE,result_dict= True)
    record = data
    if data != []:
        headings = data[0].keys()
        values = [item.values() for item in data]
    else:
        headings = ['No boosk found']
        values = []
    return render_template('allbooks.html',title = 'List of books', headings = headings, zip = zip,record = data, data = values)

@app.route('/search', methods = ['GET'])
def search():
    try:
        if request.method == 'GET':
            search = request.args.get('search')
            table = request.args.get('table')
            _filter = request.args.get('filter')
            person = request.args.get('person')
            contact = request.args.get('contact')
            titlereturn = request.args.get('title')
            print('person =',person)
            print('contact =', contact)
            if _filter == '':
                _filter == 'book_name'
            records = inventory_handler.search(search, _filter, table, person, contact)
            print(records)
            if records != []:
                headings = records[0].keys()
                data = [item.values() for item in records]
            else:
                headings = ['NO RECORD FOUND']
                data = []
            if table == INVENTORY_TABLE:
                title = 'List of books'
            elif table == BORROW_TABLE:
                title = 'Borrowed books info'
        if titlereturn == 'return':
            return render_template('returnbookdata.html',headings = headings, data = data, zip = zip,record = records, person = person, contact = contact, search = True)
        return render_template('allbooks.html',title = title, headings = headings, data = data, person = person, contact = contact, search = True)
    except Exception as e:
        print(e)

@app.route('/addbook')
def addbooks():
    return render_template('addbook.html')

@app.route('/add', methods = ['POST'])
def add():
    if request.method == 'POST':
        # id = request.form['id']
        book_name = request.form['book_name']
        author = request.form['author']
        edition = request.form['edition']
        category = request.form['category']
        description = request.form['description']
        inventory_handler.add_book_to_inventory(book_name, author, edition, category, description)
    return redirect(url_for('home'))

@app.route('/deletebook')
def delbook():
    return render_template('delbook.html')

@app.route('/delete', methods = ['POST'])
def delete():
    if request.method == 'POST':
        _id = request.form['_id']
        delete = inventory_handler.delete_record_book_inventory_table(INVENTORY_TABLE, _id)
    if delete:
        return redirect(url_for('home'))
    else:
        return '''<!doctype html>
                    <html>
                        <head>
                            <title>record not found</title>
                        </head>
                        <body>
                            <h1>record not found</h1>
                            <a href = '/home'>Go home</a>
                        </body>
                    </html>'''
                    
@app.route('/borrowbook')
def borrowbook():
    return render_template('borrowbook.html')

@app.route('/borrow', methods = ['POST'])
def borrow():
    if request.method == 'POST':
        person = request.form['p_name']
        contact = str(request.form['contact'])
        book_id = request.form['_id']
        borrow = inventory_handler.add_book_to_borrow(person = person, contact = contact, book_id = book_id)
        if borrow:
            return redirect(url_for('home'))
        else:
            return '''<!doctype html>
                    <html>
                        <head>
                            <title>book not available</title>
                        </head>
                        <body>
                            <h1>Book not available</h1>
                            <a href = '/home'>Go home</a>
                        </body>
                    </html>'''

@app.route('/borrowedbooksdata')
def borrowedbooks():
    return render_template('borrowbookrecord.html')

@app.route('/booksborrowed')
def booksborrowed():
    data = inventory_handler.get_allbooks(BORROW_TABLE, result_dict = True)
    return data

@app.route('/renderborrowbooks', methods = ['GET'])
def render_borrowed_books_data():
    # data = json_data.get_borrowed_data()
        person = request.args.get('person')
        contact = request.args.get('contact')
        data = inventory_handler.get_borrowed_books(person, contact, result_dict = True) 
        record = data
        if data != []:
            headings = data[0].keys()
            values = [item.values() for item in data]
        else:
            headings = ['NO BOOKS FOUND']
            values = []
        print('person_borrowed =', person)
        return render_template('allbooks.html',title = 'Borrowed books info', headings = headings, zip = zip,record = data, data = values, person = person, contact = contact)

@app.route('/returnbook')
def returnbook():
    return render_template('returnform.html')

@app.route('/returnbookdata', methods = ['GET'])
def returnbookdata():
    if request.method == 'GET':
        person = request.args.get('p_name')
        contact = request.args.get('contact')
        data = inventory_handler.get_borrowed_books(person, contact, result_dict = True) 
        if data != []:
            headings = data[0].keys()
            values = [item.values() for item in data]
        else:
            headings = ['NO BOOKS FOUND']
            values = []
    return render_template('returnbookdata.html',headings = headings, data = values, zip = zip,record = data, person = person, contact = contact)

@app.route('/return', methods = ['GET'])
def _return():
    if request.method == 'GET':
        borrow_id = request.args.get('_id')
        book_id = request.args.get('book_id')
        returned = inventory_handler.returnbook(borrow_id, book_id)
        if returned:
            return redirect(url_for('home'))
        return '''<!doctype html>
                    <html>
                        <head>
                            <title>data not found</title>
                        </head>
                        <body>
                            <h1>data not found</h1>
                            <a href = '/home'>Go home</a>
                        </body>
                    </html>'''
                    
@app.route('/report')
def report():
    headings =  ['Book ID', 'Book name','Author', 'Editioin', 'Category', 'count', 'No.of books available', 'Availability', 'Total borrows', 'Total returns']
    data = inventory_handler.report()
    data_weekly = [item.values() for item in data]
    data_monthly = [item.values() for item in data]
    return render_template('report.html', headings = headings, data_weekly = data_weekly, data_monthly = data_monthly )
    # return data
app.run(debug = True)