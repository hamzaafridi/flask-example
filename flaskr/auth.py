import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/register', methods=('GET','POST')) #anything that comes in to this it will reutrn value will be the return of the fucntion
def register():
    if request.method == 'POST': #validate that it's a POST request
        username = request.form['username'] #parsing the data submitted
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is requried"
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = "User {} is already registered.".format(username)
        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',(username, generate_password_hash(password))
            )
            db.commit() # push chancges to the library
            return redirect(url_for('auth.login')) #redirect response
        flash(error) #stores messages that can be retrieved when rendering HTML

    return render_template('auth/register.html') #renders a template

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        db = get_db()

        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'],password):
            error = 'Incorrect password'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id'] #data for cookie to remember user data
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None #g.user stores user data for the length of the request
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#decorator returns a new view function that wraps the original view it's applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    
    return wrapped_view