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
    

    return render_template('home.html')




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

