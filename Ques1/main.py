from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
from flask_mysqldb import MySQL
import MySQLdb.cursors
from textblob import TextBlob

app = Flask(__name__, template_folder= 'template' , static_folder='static')

app.secret_key='#the#secret#key#'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mitika@03'
app.config['MYSQL_DB'] = 'input'

mysql = MySQL(app)
print(mysql)
@app.route("/", methods = ['GET', 'POST'])
def home() :
    msg = ''
    if request.method == 'POST' :
        sentence = request.form['sentence']
        if len(sentence) > 0:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO sentiment VALUES (NULL, % s)',(sentence,))
            mysql.connection.commit()
            cursor.close()
            session['sentence'] = sentence
        edu = TextBlob(sentence)
        x = edu.sentiment.polarity
        if x < 0  :
            msg = 'Negative'
        elif x == 0 :
            msg = 'Neutral'
        else :
            msg = 'Positive'
    return render_template('home.html' , msg = msg)

app.run(debug=True) 