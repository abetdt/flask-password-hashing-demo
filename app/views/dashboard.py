"""
Dashboard views
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService
from app.services.password_service import PasswordService
from app.views.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    """Dashboard main page"""
    user = AuthService.get_current_user()
    if not user:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    
    # Get user services
    services = PasswordService.get_user_services(user.id)
    
    return render_template('dashboard/index.html', user=user, services=services)

@dashboard_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    user = AuthService.get_current_user()
    if not user:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    
    # Get user with stats
    user_data = user.to_dict(include_stats=True)
    
    return render_template('dashboard/profile.html', user=user, user_data=user_data) 