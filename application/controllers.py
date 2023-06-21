from flask import Flask, request, redirect, url_for, flash
from flask import render_template,session
from flask import current_app as app
from datetime import date,datetime
from .models import Blood, Hospital, Inventory, Donor, Seeker,Users, Transfusion, TransfusionDonor
from .models import db
from sqlalchemy import func,or_
import pywhatkit as  pwk
import keyboard as k

@app.route("/",methods = ["GET", "POST"])
def home():
    bgs = Blood.query.all()
    return render_template("index.html")

@app.route("/in",methods = ["GET", "POST"])
def blood():
    bgs = Blood.query.all()
    return render_template("blood.html")
from flask import session

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password match a user in the database
        user = Users.query.filter_by(username=username, password=password).first()
        
        if user:
            # User is authenticated, perform login actions (e.g., set session)
            session['username'] = username  # Store the username in the session
            return redirect(url_for('user_dashboard', username=username))

        else:
            # Invalid credentials, show an error message
            flash("Invalid Username/Password")
            error = "Invalid Username/Password"
            return render_template('login.html', error=error)
    
    # GET request, render the login page
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()

    # Redirect the user to the login page
    return redirect(url_for('login'))

@app.route("/about", methods = ["GET"])
def about_us():
    return render_template("about.html")

@app.route("/<username>/about", methods = ["GET",'POST'])
def about_user(username):
    return render_template("aboutlogin.html")

@app.route("/contact", methods=['GET','POST'])
def contact():
    return render_template("contact.html")

@app.route('/<username>/blood_search', methods=['GET', 'POST'])
def blood_search(username):
    if request.method == 'POST':
        blood_group = request.form.get('blood-group')
        stock = db.session.query(Blood, Inventory).join(Inventory).filter(Blood.bid == blood_group).all()
        return render_template('blood_search.html', stock=stock,username=username)
    
    return render_template('blood_search.html',username=username)
@app.route("/<username>/blood_search/<hid>/<bid>", methods=['GET', 'POST'])
def place_request(username,hid,bid):
    if request.method == 'POST':
        # Retrieve form data
        units_requested = int(request.form.get('number_units'))
        name1  = request.form.get('name')
        dob = request.form.get('dob')
        # Print the retrieved values for debugging purposes
        print(f"hid: {hid}, bid: {bid}")
        hid = int(hid)
        bid = int(bid)
        if not bid:
            return f"{hid} {bid}"
        
        h1 = Hospital.query.filter_by(hid=hid).first()
        blood1 = Blood.query.filter_by(bid=bid).first()
        user = Users.query.filter_by(username=username).first()
        if not user:
            return "Invalid user."
        # if not b_id:
            # return "Invalid Blood Group"
        # Create a new seeker
        new_seeker = Seeker(uid=user.uid, sname=name1, dob=dob, bid=bid, dolt=date.today(), mobile=user.mobile)
        db.session.add(new_seeker)
        db.session.commit()

        # Retrieve hospital and inventory details
        hospital = Hospital.query.get(h1.hid)
        inventory = Inventory.query.filter_by(hid=hid, bid=bid).first()

        if hospital and inventory:
            # Check if there are enough units in the inventory
            if inventory.stock >= units_requested:
                # Reduce the inventory stock by the requested units
                inventory.stock -= units_requested
                db.session.commit()

                # Create a new entry in the transfusion table
                new_transfusion = Transfusion(sid=new_seeker.sid, bid=bid, dot=date.today())
                db.session.add(new_transfusion)
                db.session.commit()

                flash("Booking placed successfully!")
                return redirect(f"/{username}/dashboard")
        flash("Invalid hospital or blood inventory.")
        return render_template('requestForm.html')
    return render_template('requestForm.html')

    
@app.route('/<username>/donate', methods=['GET', 'POST'])
def donate_blood(username):
    if request.method == 'POST':
        # Retrieve the selected district from the form data
        district = request.form.get('district')

        # Query the hospitals in the selected district
        hospitals = Hospital.query.filter(Hospital.loc.ilike(f'%{district}%')).all()
        # Render the template with the list of hospitals
        return render_template('donate_blood.html', hospitals=hospitals, username = username, district = district)

    # GET request, render the donate form
    return render_template('donate_blood.html')


from flask import request, render_template, flash


@app.route('/<username>/donate_form/<hid>', methods=['GET', 'POST'])
def donate_form(username, hid):
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        mobile = request.form['mobile']
        blood_group = request.form['blood-group']
        blood_group = int(blood_group)
        medical_history = request.form['medical_history']
        accept_terms = request.form.get('accept_terms')

        # Calculate age based on the provided date of birth
        today = date.today()
        age = today.year - int(dob[:4])

        if age < 18:
            flash('You must be at least 18 years old to donate blood', 'error')
            return render_template('donate_form.html')

        if not accept_terms:
            flash('Please accept the terms and conditions to proceed', 'error')
            return render_template('donate_form.html')

        # Get the uid from username in the user table
        user = Users.query.filter_by(username=username).first()
        if not user:
            flash('User not found', 'error')
            return render_template('donate_form.html')

        uid = user.uid

        # Insert the donor details into the donor table
        donor = Donor(dname=name, uid=uid, dob=dob, bid=blood_group, dold=today, mobile=mobile)
        db.session.add(donor)
        db.session.commit()

        # Update the donation details in the transfusion_donor table
        transfusion_donor = TransfusionDonor(did=donor.did, bid=blood_group, hid=hid, dot=today)
        db.session.add(transfusion_donor)
        db.session.commit()

        inventory = Inventory.query.filter_by(hid=hid, bid=blood_group).first()
        if inventory:
            inventory.stock += 1
        else:
            inventory = Inventory(hid=hid, bid=blood_group, stock=1)
            db.session.add(inventory)
        db.session.commit()

        flash('Donation details submitted successfully', 'success')
        return redirect(f"/{username}/dashboard")

    return render_template('donate_form.html')

@app.route('/<username>/your_requests', methods=['GET', 'POST'])
def prev_requests(username):
    prev_requests = db.session.query(Users.username, Seeker.sname, Blood.bgroup, Transfusion.dot).\
        join(Seeker, Users.uid == Seeker.uid).\
        join(Transfusion, Seeker.sid == Transfusion.sid).\
        join(Blood, Transfusion.bid == Blood.bid).\
        filter(Users.username == username).all()
        
    return render_template("prev_requests.html", prev_requests=prev_requests)

@app.route('/<username>/your_donations', methods=['GET', 'POST'])
def prev_donations(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        prev_donations = db.session.query(Users.username, Donor.dname, TransfusionDonor.dot, Hospital.hname, Transfusion.dot).\
            join(Donor, Donor.uid == Users.uid).\
            join(TransfusionDonor,TransfusionDonor.did == Donor.did ).\
            join(Hospital, Hospital.hid == TransfusionDonor.hid).\
            distinct().\
            all()
        return render_template("prev_donations.html", username=username, prev_donations=prev_donations)
    else:
        return "User not found"



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

        # Calculate age based on the provided date of birth
        today = date.today()
        dob_date = datetime.strptime(dob, '%Y-%m-%d').date()
        age = today.year - dob_date.year
        if today < dob_date.replace(year=today.year):
            age -= 1

        if age < 18:
            flash('You must be at least 18 years old to sign up')
            return render_template('signup.html')

        new_user = Users(username=username, password=password, dob=dob, mobile=mobile, email=email)
        db.session.add(new_user)
        db.session.commit()
        whatsapp_number = f"+91{mobile}"  # Replace with the recipient's WhatsApp number
        message = "Welcome to blood Connect. Login using your credentials now to further explore our features!\n"
        
        try:
            pwk.sendwhatmsg_instantly(whatsapp_number, message)
            k.press_and_release('enter')
            print("WhatsApp message sent successfully")
        except Exception as e:
            print(f"Failed to send WhatsApp message: {str(e)}")

        return redirect('/login')

    return render_template('signup.html')

@app.route('/<username>/dashboard', methods=['GET', 'POST'])
def user_dashboard(username):
    # Access the username from the session
    username = session['username']
    
    return render_template('dashboard.html', username=username)


