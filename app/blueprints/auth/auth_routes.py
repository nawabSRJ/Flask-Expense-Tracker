from flask import Blueprint, request, redirect, url_for, render_template, flash, session
from db_ops import signup_user, existing_email, find_user
from werkzeug.security import check_password_hash, generate_password_hash


auth_bp =  Blueprint('auth', __name__ ,url_prefix='/auth')


# ================ Helper functions ================

def validate_user(user):
    """
    Validates user signup data.
    Returns:
        {
            "error": bool,
            "message": str
        }
    """

    # Remove leading/trailing spaces
    name = user["name"].strip()
    email = user["email"].strip().lower()
    phone = user["phone"].strip()
    password = user["password"]
    confirm_password = user["confirm_password"]
    gender = user["gender"]
    dob = user["dob"]

    
    # Empty fields

    required_fields = {
        "Name": name,
        "Email": email,
        "Password": password,
        "Confirm Password": confirm_password,
        "Phone": phone,
        "Gender": gender,
        "Date of Birth": dob
    }

    for field_name, value in required_fields.items():
        if not value:
            return {
                "error": True,
                "message": f"{field_name} is required."
            }


    # Name
    if len(name) < 3:
        return {
            "error": True,
            "message": "Name must contain at least 3 characters."
        }


    # Phone
    if not phone.isdigit() or len(phone) != 10:
        return {
            "error": True,
            "message": "Phone number must contain exactly 10 digits."
        }


    # Password
    if len(password) < 8:
        return {
            "error": True,
            "message": "Password must be at least 8 characters long."
        }

    if password != confirm_password:
        return {
            "error": True,
            "message": "Passwords do not match."
        }

    return {
        "error": False,
        "message": "Success"
    }





@auth_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        user = dict(
        name = request.form.get('name'),
        email = request.form.get('email'),
        password = request.form.get('password'),
        confirm_password = request.form.get('confirm_password'),
        phone = request.form.get('phone'),
        gender = request.form.get('gender'),
        dob = request.form.get('dob')
        )


        # basic validation
        check = validate_user(user)
        if check['error']:
            flash(check['message'], 'danger')
            return render_template("auth/signup.html")
        
        # check for existing email 
        email_exists = existing_email(user['email'])
        if email_exists:
            flash('Email already exists! SignUp with a different email.', 'danger')
            return render_template("auth/signup.html")
        

        # generate password hash
        user['password_hash'] = generate_password_hash(user['password'])
        user.pop('confirm_password')    # no need for this now

        del user["password"]

        # send to signup function
        db_insert = signup_user(user)
        if db_insert:
            flash("Account created successfully.", "success")
            return redirect(url_for("auth.login"))
        

    flash("Some Error Occurred", "danger")
    return render_template("auth/signup.html")



@auth_bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        # verify credentials and login
        email = request.form.get('email')
        password = request.form.get('password')
        
        db_lookup = find_user(email,password)

        if db_lookup['error']:
            flash('No such user found', 'danger')
            return redirect(url_for('auth.login'))
        
        user = db_lookup['row']
        # start session
        session['user'] = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'phone': user['phone'],
            'gender': user['gender'],
            'dob': user['dob']
        }

        return redirect(url_for('user.dashboard'))


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))