from flask import *
# create a flask application
app = Flask(__name__)
# above __name__ means this is now your main app



# Database  NorthWind
# Table Items
# Host   -  localhost
# Username   root
# Password  not set

import pymysql
@app.route('/')
def home():
    # Connect to database
    connection = pymysql.connect(host='localhost', user='root',password='',
                                 database='NorthWind')

    # Create a cursor to execute SQL Query
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Items')
    # AFter executing the query above, get all rows
    rows = cursor.fetchall()

    # after getting the rows forward them to home.html for users to see them
    return render_template('home.html', rows = rows)




# we create a /single
# this route will search a product with this product id
@app.route('/single/<id>')
def single(id):
    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='NorthWind')

    # Create a cursor to execute SQL Query
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Items')
    # AFter executing the query above, get all rows
    rows = cursor.fetchall()

    # after getting the rows forward them to home.html for users to see them
    return render_template('home.html', rows=rows)








@app.route('/login')
def login():
    return 'This is a login .. '


@app.route('/register')
def register():
    return 'This is going to be registration'


@app.route('/profile')
def profile():
    return 'This is my Profile'



# confirm if __name__ is equal __main__
if __name__ == '__main__':
    app.run(debug=True)

