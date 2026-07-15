from flask import Blueprint, request, render_template

auth_bp =  Blueprint('auth', __name__ ,url_prefix='/auth')


@auth_bp.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        # POST data to DB
        pass
    pass
