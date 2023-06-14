from flask import Flask, request, redirect, url_for, flash
from flask import render_template
from flask import current_app as app
from datetime import date
from .models import Blood, Hospital, Inventory, Donor, Seeker,Users, Transfusion
from .models import db

@app.route("/",methods = ["GET", "POST"])
def home():
    bgs = Blood.query.all()
    return render_template("index.html")

@app.route("/in",methods = ["GET", "POST"])
def blood():
    bgs = Blood.query.all()
    return render_template("blood.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match a user in the database
        user = Users.query.filter_by(username=username, password=password).first()
        
        if user:
            # User is authenticated, perform login actions (e.g., set session)
            # Redirect to a logged-in page
            return redirect(url_for('user_dashboard',username = username))

        else:
            # Invalid credentials, show an error messaged                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    
    # GET request, render the login page
    return render_template('login.html')
@app.route("/about", methods = ["GET"])
def about_us():
    return render_template("about.html")

@app.route("/<username>/about", methods = ["GET",'POST'])
def about_user(username):
    return render_template("about.html")

@app.route("/contact", methods=['GET','POST'])
def contact():
    return render_template("contact.html")

@app.route('/<username>/blood_search', methods=['GET', 'POST'])
def blood_search(username):
    if request.method == 'POST':
        blood_group = request.form.get('blood-group')
        stock = db.session.query(Blood, Inventory).join(Inventory).filter(Blood.bgroup == blood_group).all()
        return render_template('blood_search.html', stock=stock,username=username)
    
    return render_template('blood_search.html',username=username)

@app.route("/<username>/placerequest", methods = ['GET','POST'])
def place_request(username,hid,bid): 
    if request.method == 'GET':
        hospital_id = hid
        blood_group = bid
        return render_template('requestForm.html')

    elif request.method == 'POST':
        # Retrieve form data
        
        units_requested = int(request.form.get('number_units'))

        # Retrieve hospital and inventory details
        hospital = Hospital.query.get(hospital_id)
        inventory = Inventory.query.filter_by(hid=hospital_id, bid=blood_group).first()

        if hospital and inventory:
            # Check if there are enough units in the inventory
            if inventory.stock >= units_requested:
                # Reduce the inventory stock by the requested units
                inventory.stock -= units_requested
                db.session.commit()

                # Create a new entry in the transfusion table
                new_transfusion = Transfusion(sid=Seeker.sid, bid=blood_group, dot=date.today())
                db.session.add(new_transfusion)
                db.session.commit()

                # Perform any additional actions or redirection
                # ...

                return "Request placed successfully."

        return "Invalid hospital or blood inventory."

    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dob = request.form['dob']
        mobile = request.form['mobile']
        email = request.form['email']
        
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return render_template('signup.html')
        
        new_user = Users(username=username, password=password, dob=dob, mobile=mobile, email=email)
        db.session.add(new_user)
        db.session.commit()
      
            
        return redirect('/login')
    
    return render_template('signup.html')
@app.route('/<username>/dashboard', methods=['GET', 'POST'])
def user_dashboard(username):
    return render_template('dashboard.html', username=username)
