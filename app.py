from models import db, User
from flask import Flask, request, jsonify, render_template
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = "xinchao_secure_key_2025"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Khoi tao database
db.init_app(app)

# Tao tat ca table dc dinh nghia models
# Chi tao table chua ton tai
with app.app_context():
    db.create_all()

#Home page
@app.route("/")
def home():
    # Kiểm tra user_id có hợp lệ không
    if "user_id" in session:
        try:
            user_id = session["user_id"]
            user = User.query.get(user_id)

            #Neu user khong ton tai, khong active
            if not user or not user.is_active:
                session.clear()
                flash("Phien dang nhap khong hop le. Vui long dang nhap lai:", "waring")
                return render_template("home.html")
            return redirect(url_for("dashboard"))
        except Exception as e:
            # Log error và clear session
            app.logger.error(f"Error checking user session: {e}")
            session.clear()
            return render_template("home.html")
    return render_template("home.html")

#Sign up
# 1. TẠO USER MỚI
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Kiểm tra user đã tồn tại chưa
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'error': 'Username đã tồn tại'}), 400

    # Tạo user mới
    new_user = User(
        username=data['username'],
        email=data['email']
    )
    new_user.set_password(data['password'])  # Hash password

    # Lưu vào database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Đăng ký thành công', 'user': new_user.to_dict()}), 201

#Hepler functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    match = re.match(pattern, email)
    if match is not None:
        return True
    return False

def validate_password(password):
    """Mật khẩu tối thiểu 6 ký tự, có ít nhất 1 chữ cái và 1 số"""
    if len(password) < 6:
        return False
    if not re.search(r"[A-Za-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True

def validate_username(username):
    """Chỉ cho phép chữ cái, số và dấu gạch dưới"""
    return re.match(r'^\w+$', username) is not None


# 2. ĐĂNG NHẬP
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Tên người dùng không tồn tại"}), 400

    if not user.check_password(password):
        return jsonify({"error": "Mật khẩu không chính xác"}), 400

    if not user.is_active:
        return jsonify({"error": "Tài khoản bị khóa hoặc không hoạt động"}), 403

    # Cập nhật phiên đăng nhập
    user.update_last_login()
    session["user_id"] = user.id

    return jsonify({"message": "Đăng nhập thành công", "user": user.to_dict()}), 200

# 3. ĐĂNG XUẤT
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Đăng xuất thành công"}), 200
