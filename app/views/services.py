"""
Service management views
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.auth_service import AuthService
from app.services.password_service import PasswordService
from app.views.auth import login_required

services_bp = Blueprint('services', __name__)

@services_bp.route('/add_service', methods=['POST'])
@login_required
def add_service():
    """Add new service"""
    user = AuthService.get_current_user()
    if not user:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    
    # Get form data
    service_data = {
        'service_name': request.form['service_name'],
        'service_username': request.form['service_username'],
        'service_url': request.form.get('service_url', ''),
        'notes': request.form.get('service_note', ''),
        'service_password': request.form['service_password']
    }
    
    # Add service
    success, error_message = PasswordService.add_service(
        user.id, 
        service_data, 
        user.password_hash
    )
    
    if success:
        flash('Thêm dịch vụ thành công!', 'success')
    else:
        flash(error_message, 'error')
    
    return redirect(url_for('dashboard.index'))

@services_bp.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    """Edit service"""
    user = AuthService.get_current_user()
    if not user:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    
    service = PasswordService.get_service(service_id, user.id)
    if not service:
        flash('Dịch vụ không tồn tại.', 'error')
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        # Get form data
        service_data = {
            'service_name': request.form['service_name'],
            'service_username': request.form['service_username'],
            'service_url': request.form.get('service_url', ''),
            'notes': request.form.get('service_note', ''),
            'service_password': request.form['service_password']
        }
        
        # Update service
        success, error_message = PasswordService.update_service(
            service_id, 
            user.id, 
            service_data, 
            user.password_hash
        )
        
        if success:
            flash('Cập nhật dịch vụ thành công!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash(error_message, 'error')
    
    return render_template('services/edit.html', user=user, service=service)

@services_bp.route('/service/<int:service_id>')
@login_required
def service_detail(service_id):
    """Service detail page"""
    user = AuthService.get_current_user()
    if not user:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    
    service = PasswordService.get_service(service_id, user.id)
    if not service:
        flash('Dịch vụ không tồn tại.', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Get decrypted password
    decrypted_password = PasswordService.get_service_password(
        service_id, 
        user.id, 
        user.password_hash
    )
    
    return render_template(
        'services/detail.html',
        user=user,
        service=service,
        decrypted_password=decrypted_password
    )

@services_bp.route('/delete_service/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    """Delete service (soft delete)"""
    user = AuthService.get_current_user()
    if not user:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('auth.login'))
    
    success, error_message = PasswordService.delete_service(service_id, user.id)
    
    if success:
        flash('Dịch vụ đã được ẩn khỏi danh sách (xóa mềm).', 'success')
    else:
        flash(error_message, 'error')
    
    return redirect(url_for('dashboard.index')) 