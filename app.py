from flask import *
# create a flask application
app = Flask(__name__)
# above __name__ means this is now your main app

@app.route('/')
def home():
    # Connect to database
    conn = pymysql.connect(host="localhost", user="root", password="", database="NorthWind")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from Items")
    # check if no records were found
    rows = cursor.fetchall()
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


import pymysql
@app.route('/products')
def products():
    # Connect to database
    conn = pymysql.connect(host="localhost", user="root", password="", database="NorthWind")
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from Items")
    # check if no records were found
    rows = cursor.fetchall()
    return render_template('products.html', rows=rows)



# confirm if __name__ is equal __main__
if __name__ == '__main__':
    app.run(debug=True)

