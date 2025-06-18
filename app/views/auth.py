"""
Authentication views
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AuthService.is_authenticated():
            flash('Vui lòng đăng nhập.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def redirect_if_authenticated(f):
    """Decorator to redirect authenticated users"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if AuthService.is_authenticated():
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/')
def index():
    """Home page - redirect to dashboard if logged in, otherwise to login"""
    if AuthService.is_authenticated():
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
@redirect_if_authenticated
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, error_message = AuthService.login_user(username, password)
        
        if success:
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash(error_message, 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
@redirect_if_authenticated
def register():
    """Register page"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success, error_message = AuthService.register_user(username, email, password)
        
        if success:
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(error_message, 'error')
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout user"""
    AuthService.logout_user()
    flash('Đã đăng xuất.', 'success')
    return redirect(url_for('auth.login')) 