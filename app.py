from flask import *
# create a flask application
app = Flask(__name__)
# above __name__ means this is now your main app

@app.route('/')
def home():
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

