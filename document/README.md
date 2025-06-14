# Hướng dẫn làm việc nhóm với Git

## Quy trình làm việc

Mỗi thành viên làm theo các bước sau:

### 1. Clone repository

```bash
git clone https://github.com/abetdt/flask-password-hashing-demo.git
cd flask-password-hashing-demo
```

### 2. Tạo nhánh riêng cho mỗi người

Ví dụ:

* Người 1 làm phần xác thực:

  ```bash
  git checkout -b nguoi1-auth
  ```

* Người 3 làm phần giao diện (frontend):

  ```bash
  git checkout -b nguoi3-frontend
  ```

> Lưu ý: Tên nhánh nên đặt theo format `tennguoi-congviec` để dễ quản lý.

### 3. Làm việc trên nhánh của bạn

Sau khi chỉnh sửa, hãy commit và push:

```bash
git add .
git commit -m "Thêm chức năng đăng ký và hash mật khẩu"
git push origin nguoi1-auth
```

### 4. Tạo Pull Request

Sau khi push lên GitHub, vào repository và tạo **Pull Request** từ nhánh của bạn vào `main`.

> Một người khác trong nhóm sẽ kiểm tra, góp ý, rồi mới **merge** vào nhánh chính `main`.

---

## Gợi ý tên nhánh cho các thành viên

| Thành viên | Phân công                         | Tên nhánh gợi ý   |
| ---------- |-----------------------------------|-------------------|
| Người 1    | Đăng ký / đăng nhập, cơ sở dữ liệu | `nguoi1-auth`     |
| Người 2    | Hàm băm dùng, salt, bảo mật       | `nguoi2-hash`     |
| Người 3    | Giao diện frontend                | `nguoi3-frontend` |
| Người 4    | Làm slide, viết tài liệu          | `nguoi4-document` |



---

## Lưu ý chung

* Luôn làm việc trên nhánh riêng, **không sửa trực tiếp `main`**.
* Pull thường xuyên để cập nhật thay đổi từ các bạn khác.
* Commit phải có nội dung rõ ràng.
* Trước khi merge vào `main`, luôn tạo Pull Request để mọi người review.

---


