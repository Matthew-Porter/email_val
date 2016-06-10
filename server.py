from flask import Flask, request, redirect, render_template, flash, session
from mysqlconnection import MySQLconnector
import re 
from time import gmtime, strftime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "donttellanyonethis"

mysql = MySQLConnector(app, 'email_validation')

@app.route('/')
def index():
	# print 'test'

	return render_template('index.html')
@app.route('/emails', methods=['Post'])
def emailval():
	if not EMAIL_REGEX.match(request.form['email']):
		flash("Please check email", 'error')
		return redirect('/')
	else:
		query = 'INSERT INTO emails (email, created_at, updated_at) VALUES (:email, NOW(), NOW())'
		data = {
			'email': request.form['email']
		}
		mysql.query_db(query, data)
		flash('Email {} is valid!'.format(request.form['email']), 'sucess')
		return redirect('/sucess')
@app.route('/success', methods=['GET'])
def show():
	query = "SELECT * FROM emails"
	emails = mysql.query_db(query)
	return render_template('success.html', all_emails = emails)

@app.route('/destroy/<email_id>', methods=['POST'])
def delete(email_id):
	query = "DELETE FROM emails WHERE id = :id"
	data = {'id': email_id}
	mysql.query_db(query, data)
	return redirect('/success')


app.run(debug=True)