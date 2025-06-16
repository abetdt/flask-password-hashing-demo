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
    # Kiểm tra nếu user đã đăng nhập thì redirect về dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
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
    # Kiểm tra nếu user đã đăng nhập thì redirect về dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
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

    # Tạo service mới
    service = Service(
        user_id=user.id,
        service_name=request.form['service_name'],
        service_username=request.form['service_username'],
        service_url=request.form.get('service_url', ''),     # nếu có input này
        notes=request.form.get('service_note', '')           # sửa lại từ 'note' → 'notes'
    )

    # Mã hoá mật khẩu
    service.set_service_password(request.form['service_password'], user.password_hash)

    # Lưu vào DB
    db.session.add(service)
    db.session.commit()

    flash('Thêm dịch vụ thành công!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/edit_service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    service = Service.query.get(service_id)

    if service is None or service.user_id != user.id:
        flash('Dịch vụ không tồn tại.', 'error')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        service.service_name = request.form['service_name']
        service.service_username = request.form['service_username']
        service.notes = request.form.get('service_note', '')  # ✅ đổi note → notes
        service.set_service_password(request.form['service_password'], user.password_hash)
        db.session.commit()

        flash('Cập nhật dịch vụ thành công!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_service.html', user=user, service=service)


@app.route("/service/<int:service_id>")
def service_detail(service_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    service = Service.query.get(service_id)

    # ✅ Kiểm tra thêm cả is_active
    if service is None or service.user_id != user.id or not service.is_active:
        flash('Dịch vụ không tồn tại.', 'error')
        return redirect(url_for('dashboard'))

    # ✅ Giải mã mật khẩu và gửi sang template
    decrypted_password = service.get_service_password(user.password_hash)
    print(f"Decrypted password for service {service_id}: {decrypted_password}")
    return render_template(
        'service_detail.html',
        user=user,
        service=service,
        decrypted_password=decrypted_password
    )




@app.route('/delete_service/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    if 'user_id' not in session:
        flash('Vui lòng đăng nhập.', 'error')
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    service = Service.query.get(service_id)

    if service is None or service.user_id != user.id:
        flash('Dịch vụ không tồn tại hoặc bạn không có quyền xoá.', 'error')
        return redirect(url_for('dashboard'))

    # ✅ Xóa mềm: chỉ đổi cờ is_active
    service.is_active = False
    db.session.commit()

    flash('Dịch vụ đã được ẩn khỏi danh sách (xóa mềm).', 'success')
    return redirect(url_for('dashboard'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    app.run(debug=True, host='0.0.0.0', port=5000)