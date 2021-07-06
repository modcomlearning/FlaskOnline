from flask import *
# create a flask application
app = Flask(__name__)
# above __name__ means this is now your main app

# User sessions is unique variable given to user and used after a successful login
# a session key makes the logged identified by the system
# this key needs to be created after successful login
# To create secure sessions set a strong encryption key
app.secret_key = '12WEhr&88?8J*&9_'

# Database  NorthWind
# Table Items
# Host   -  localhost
# Username   root
# Password  not set
# Task  - creating more products
# in your database create a table  of your choice, in my case 'bikes'
# columns
# ProductID, INT(10) PK - AI
# ProductName,  VARCHAR(50)
# ProductDesc, VARCHAR(50)
# ProductCategory, VARCHAR(50)
# ProductCost, VARCHAR(50)
# PrevCost,VARCHAR(50)
# ProductImage VARCHAR(300)
# DateAdded DATE(50)

# Add 5 6 products
# For image get a link online, a link ending with /png, jpg, jpeg, webp
# or use modcom.co.ke/pics/
#
# step 2
# create a route to fetch this products as rows
# Create a template and bind the rows
# NB: refer how home page was done







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


@app.route('/bikes')
def bikes():
    # Connect to database
    connection = pymysql.connect(host='localhost', user='root',password='',
                                 database='NorthWind')

    # Create a cursor to execute SQL Query
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM bikes')
    # AFter executing the query above, get all rows
    rows = cursor.fetchall()

    # after getting the rows forward them to home.html for users to see them
    return render_template('bikes.html', rows = rows)


# we create a /single
# this route will search a product with this product id
@app.route('/single/<id>')
def single(id):

    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='NorthWind')

    # Create a cursor to execute SQL Query
    cursor = connection.cursor()

    # below %s is a place holder for id
    cursor.execute('SELECT * FROM Items WHERE ProductID = %s', (id))
    # AFter executing the query above, get one row because
    row = cursor.fetchone()

    # after getting the row forward it to single.html for users to see it
    return render_template('single.html', row=row)



@app.route('/singlebikes/<id>')
def singlebikes(id):

    connection = pymysql.connect(host='localhost', user='root', password='',
                                 database='NorthWind')

    # Create a cursor to execute SQL Query
    cursor = connection.cursor()

    # below %s is a place holder for id
    cursor.execute('SELECT * FROM bikes WHERE ProductID = %s', (id))
    # AFter executing the query above, get one row because
    row = cursor.fetchone()

    # after getting the row forward it to single.html for users to see it
    return render_template('singlebikes.html', row=row)








@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        phone = request.form['phone']

        # check if passwords are same
        import re
        if password != confirm:
            return  render_template('signup.html', msg = 'Password Not matching')
        elif len(password)  < 8:
            return render_template('signup.html', msg = 'Must be more than 8 -xters')

        else:
            connection = pymysql.connect(host='localhost', user='root',
                                         password='',database='appledb')
            cursor = connection.cursor()


            cursor.execute('insert into shop_users(email,password,phone)values(%s,%s,%s)',
                               (email, password, phone))
            # we need to make a commit to changes to dbase
            connection.commit()
            return render_template('signup.html', success = 'Thank you for Joining')


    else: # this means POST was not used, show the signup template
        return  render_template('signup.html')


# create a route for login
@app.route('/signin', methods = ['POST','GET'])
def signin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        # process login
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='appledb')

        # Create a cursor to execute SQL Query
        cursor = connection.cursor()
        cursor.execute('select * from shop_users where email = %s and password =%s',
                       (email, password))
        # above query should either find a match or not
        # check how may rows cursor found
        if cursor.rowcount ==0:
            return render_template('signin.html', error = 'Wrong Credentials!')

        elif cursor.rowcount ==1:
            session['key'] = email
            return redirect('/')
        else:
            return render_template('signin.html', error = 'Something went wrong')

    else:
        return render_template('signin.html')


@app.route('/signout')
def signout():
    session.pop('key', None)
    return redirect('/')   # take user to home route after logout



# modcom.co.ke/sql/payment
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/payment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "10",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "Modcom",
            "TransactionDesc": "Modcom"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return render_template('mpesa_payment.html', msg='Please Complete Payment in Your Phone')
    else:
        return render_template('mpesa_payment.html')


# confirm if __name__ is equal __main__
if __name__ == '__main__':
    app.run(debug=True)

