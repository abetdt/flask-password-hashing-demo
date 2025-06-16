function checkPassword() {
    console.log("checkPassword called"); // Debug
    const password = document.getElementById('password').value;
    const strengthText = document.getElementById('password-strength');

    if (password.length < 8) {
        strengthText.textContent = 'Mật khẩu yếu (ít nhất 8 ký tự).';
        strengthText.style.color = 'red';
    } else if (!/[A-Z]/.test(password) || !/[0-9]/.test(password) || !/[!@#$%^&*]/.test(password)) {
        strengthText.textContent = 'Mật khẩu nên có chữ hoa, số và ký tự đặc biệt.';
        strengthText.style.color = 'orange';
    } else {
        strengthText.textContent = 'Mật khẩu mạnh.';
        strengthText.style.color = 'green';
    }
}

function generatePassword() {
    console.log("generatePassword called"); // Debug
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < 12; i++) {
        password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    const passwordInput = document.getElementById('password');
    passwordInput.value = password;
    checkPassword(); // Gọi lại để cập nhật thông báo độ mạnh
}
function togglePassword(inputId, buttonId) {
    console.log("togglePassword called"); // Debug
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    if (input.type === "password") {
        input.type = "text";
        button.textContent = "Ẩn";
    } else {
        input.type = "password";
        button.textContent = "Hiển thị";
    }
}