from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to MongoDB database
client = MongoClient('mongodb+srv://SwapnilSethi:La6r8Stu9AGqJbr@mongodbclusterforbdapro.4re5jyl.mongodb.net/test')
db = client['BeyondPrice']
users_collection = db['Credentials']

# Create Flask app
app = Flask(__name__)

# Define routes for landing pages
@app.route('/')
def welcome():
    return render_template('main.html')
    #return render_template('login.html')
'''
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
'''
#@app.route("/signup1", methods=["GET", "POST"])
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        # Get user input from the form
        FirstName = request.form["firstname"]
        print(request.form["firstname"])
        LastName = request.form["lastname"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        # Insert user data into the database
        user_data = {"firstname": FirstName, "lastname": LastName, "email": email, "password": password, "phone": phone, "confirmpassword": confirmpassword}
        print(user_data)
        users_collection.insert_one(user_data)
        print(user_data)
        # Redirect to the main page
        #return redirect(url_for("signup1"))
        return render_template("main.html")
        #return 'User signed up successfully!'
    else: return render_template('signup.html')


@app.route('/login', methods=["GET","POST"])
def login():
    # Get user data from request body
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        # Find user in database
        user = users_collection.find({"email": email, "passowrd":password})
        print(user)
        # Check if user exists and password is correct
        if user:
            return 'Logged in successfully!'
        else:
            return 'Invalid credentials. Please try again.'
    else:
        return render_template('login.html')
# Run the Flask app
if __name__ == '__main__':
    app.run()
