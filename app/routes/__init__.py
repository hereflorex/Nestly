from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.models import User, Room

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', user=session.get('username'))


@main.route('/auth', methods=['GET', 'POST'])
def auth():
    mode = request.args.get('mode', 'login')
    if request.method == 'POST':
        mode = request.form.get('mode', 'login')
        username = request.form.get('username', '').strip().lower()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if mode == 'signup':
            if not username or not email or len(password) < 8:
                flash('Use a username, valid email and password of at least 8 characters.', 'error')
                return redirect(url_for('main.auth', mode='signup'))
            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash('Username or email already exists.', 'error')
                return redirect(url_for('main.auth', mode='signup'))
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('main.dashboard'))

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Incorrect email or password.', 'error')
            return redirect(url_for('main.auth', mode='login'))
        if user.is_banned:
            flash('This account is currently restricted.', 'error')
            return redirect(url_for('main.auth'))
        session.clear()
        session['user_id'] = user.id
        session['username'] = user.username
        session['role'] = user.role
        return redirect(url_for('main.dashboard'))

    return render_template('auth.html', mode=mode)


@main.route('/dashboard')
def dashboard():
    if not session.get('user_id'):
        return redirect(url_for('main.auth'))
    return render_template('dashboard.html', username=session.get('username'), role=session.get('role'))


@main.route('/rooms/create', methods=['POST'])
def create_room():
    if not session.get('user_id'):
        return redirect(url_for('main.auth'))
    room = Room(code=Room.new_code(), owner_id=session['user_id'])
    db.session.add(room)
    db.session.commit()
    return redirect(url_for('main.room', code=room.code))


@main.route('/rooms/<code>')
def room(code):
    room_obj = Room.query.filter_by(code=code, is_active=True).first_or_404()
    return render_template('room.html', room=room_obj, username=session.get('username', 'Guest'))


@main.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


@main.app_context_processor
def inject_globals():
    return {'current_user_id': session.get('user_id'), 'current_role': session.get('role')}
