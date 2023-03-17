from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to MongoDB database
client = MongoClient('mongodb+srv://SwapnilSethi:La6r8Stu9AGqJbr@mongodbclusterforbdapro.4re5jyl.mongodb.net/test')
db = client['<BDAProject1>']
users_collection = db['users']

# Create Flask app
app = Flask(__name__)

# Define routes for landing pages
@app.route('/')
def welcome():
    return render_template('main.html')
'''
@app.route('/signup')
def signup():
    return render_template('signup.html')
'''
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Get user input from the form
        FirstName = request.form["First Name"]
        LastName = request.form["Last Name"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["Phone Number"]
        
        # Insert user data into the database
        user_data = {"firstname": FirstName, "lastname": LastName, "email": email, "password": password, "phone": phone}
        users_collection.insert_one(user_data)
        
        # Redirect to the main page
        return redirect(url_for("main"))
    else:
        return render_template("signup.html")


@app.route('/signin', methods=['POST'])
def signin():
    # Get user data from request body
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Find user in database
    user = users_collection.find_one({'username': username})

    # Check if user exists and password is correct
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# Run the Flask app
if __name__ == '__main__':
    app.run(port=8080)
