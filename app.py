from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Service
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'hi')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Sử dụng SQLite cho đơn giản
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Tạo database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.find_by_username(username)
        if user and user.verify_password(password):
            session['user_id'] = user.id
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu sai.', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.find_by_username(username) or User.find_by_email(email):
            flash('Tên đăng nhập hoặc email đã tồn tại.', 'error')
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Đã đăng xuất.', 'success')
    return redirect(url_for('login'))

@app.route('/add_service', methods=['POST'])
def add_service():
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    service = Service(
        user_id=user.id,
        service_name=request.form['service_name'],
        service_username=request.form['service_username']
    )
    service.set_service_password(request.form['service_password'], user.password_hash)
    db.session.add(service)
    db.session.commit()
    flash('Thêm dịch vụ thành công!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)