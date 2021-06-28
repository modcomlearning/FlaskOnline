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


# This routes reads products based on id
@app.route('/single/<id>')
def purchase(id):
    conn = pymysql.connect(host='localhost', user='root', password='',
                                 database='NorthWind')
    cursor = conn.cursor()
    # execute the query using the cursor
    cursor.execute("select * from Items where ProductID = %s", (id))
    # check if no records were found
    if cursor.rowcount < 1:
        return render_template('single.html', msg="This Product does not exist")
    else:
        # return all rows found
        rows = cursor.fetchone()
        return render_template('single.html', rows=rows)



# Mpesa
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa_payment', methods = ['POST','GET'])
def mpesa_payment():

        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            #GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
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
                "Amount": "1",  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return render_template('mpesa_payment.html', msg = 'Please Complete Payment in Your Phone')
        else:
            return render_template('mpesa_payment.html')






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

