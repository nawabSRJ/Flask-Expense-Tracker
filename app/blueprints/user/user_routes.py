from flask import Blueprint, request, render_template, session

user_bp = Blueprint('user', __name__, url_prefix='/user')



@user_bp.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'GET':
        user = session.get('user')
        return render_template('user/dashboard.html', user=user)
    else:
        return '<h1> Error rendering dashboard </h1>'