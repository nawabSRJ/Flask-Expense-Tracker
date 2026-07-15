from flask import Blueprint, request, render_template
from db_ops import signup_user


auth_bp =  Blueprint('auth', __name__ ,url_prefix='/auth')


@auth_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        user_dict = dict(
        name = request.form.get('name'),
        email = request.form.get('email'),
        password = request.form.get('password'),
        confirm_password = request.form.get('confirm_password'),
        phone = request.form.get('phone'),
        gender = request.form.get('gender'),
        dob = request.form.get('dob')
        )
        # how do we manage profile picture here?

        # basic validation

        # send to signup function
        signup_user(user_dict)
        pass
    pass
