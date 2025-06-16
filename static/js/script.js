// Kiểm tra xem username có hợp lệ không?
function validateUsername() {
    const username = document.getElementById('username').value;
    const errorElement = document.getElementById('username-error');
    
    // Xóa thông báo lỗi cũ
    errorElement.textContent = '';
    
    if (!username) {
        errorElement.textContent = 'Tên đăng nhập không được để trống';
        return false;
    }
    
    // Kiểm tra độ dài tối thiểu
    if (username.length < 4) {
        errorElement.textContent = 'Tên đăng nhập phải có ít nhất 4 ký tự';
        return false;
    }
    
    // Kiểm tra độ dài tối đa
    if (username.length > 20) {
        errorElement.textContent = 'Tên đăng nhập không được quá 20 ký tự';
        return false;
    }
    
    // Kiểm tra ký tự đầu phải là chữ cái
    if (!/^[a-zA-Z]/.test(username)) {
        errorElement.textContent = 'Tên đăng nhập phải bắt đầu bằng chữ cái';
        return false;
    }
    
    // Kiểm tra chỉ chứa chữ cái, số, dấu gạch dưới hoặc dấu chấm
    if (!/^[a-zA-Z][a-zA-Z0-9._]*$/.test(username)) {
        errorElement.textContent = 'Tên đăng nhập chỉ được chứa chữ cái, số, dấu gạch dưới (_) và dấu chấm (.)';
        return false;
    }
    
    // Nếu tất cả đều hợp lệ
    errorElement.innerHTML = '<span style="color: #00aa00;">✓ Tên đăng nhập hợp lệ</span>';
    return true;
}

//Kiểm tra email có hợp lệ không?
function validateEmail() {
    const email = document.getElementById('email').value;
    const errorElement = document.getElementById('email-error');
    
    // Xóa thông báo lỗi cũ
    errorElement.textContent = '';
    
    if (!email) {
        errorElement.textContent = 'Email không được để trống';
        return false;
    }
    
    // Regex kiểm tra định dạng email chuẩn
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    
    if (!emailRegex.test(email)) {
        errorElement.textContent = 'Định dạng email không hợp lệ (ví dụ: user@example.com)';
        return false;
    }
    
    // Kiểm tra thêm các ràng buộc khác
    if (email.length > 100) {
        errorElement.textContent = 'Email không được quá 100 ký tự';
        return false;
    }
    
    // Kiểm tra không có hai dấu chấm liên tiếp
    if (email.includes('..')) {
        errorElement.textContent = 'Email không được chứa hai dấu chấm liên tiếp';
        return false;
    }
    
    // Nếu tất cả đều hợp lệ
    errorElement.innerHTML = '<span style="color: #00aa00;">✓ Email hợp lệ</span>';
    return true;
}

// function validateForm() {
//     const isUsernameValid = validateUsername();
//     const isEmailValid = validateEmail();
//     const isPasswordValid = checkPasswordStrength();
//     const isPasswordMatch = checkPasswordMatchValidation();
    
//     // Chỉ cho phép submit khi tất cả đều hợp lệ
//     return isUsernameValid && isEmailValid && isPasswordValid && isPasswordMatch;
// }

function checkPasswordStrength() {
    const password = document.getElementById('password').value;
    
    if (!password) {
        return false;
    }
    
    // Kiểm tra các tiêu chí mật khẩu mạnh
    const criteria = {
        length: password.length >= 8,
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
    };
    
    const passedCriteria = Object.values(criteria).filter(Boolean).length;
    
    // Yêu cầu ít nhất 4 tiêu chí được đáp ứng
    return passedCriteria >= 4;
}

function checkPasswordMatchValidation() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    
    return password && confirmPassword && password === confirmPassword;
}

// Cập nhật hàm checkPassword để tích hợp validation
function checkPassword() {
    console.log("checkPassword called");
    const password = document.getElementById('password').value;
    const strengthText = document.getElementById('password-strength');
    
    if (!password) {
        strengthText.textContent = '';
        checkPasswordMatch();
        return;
    }
    
    const criteria = {
        length: password.length >= 8,
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
    };
    
    const passedCriteria = Object.values(criteria).filter(Boolean).length;
    
    let strength, color, score;
    
    if (passedCriteria <= 2) {
        strength = 'Rất yếu';
        color = '#ff4444';
        score = 1;
    } else if (passedCriteria === 3) {
        strength = 'Yếu';
        color = '#ff8800';
        score = 2;
    } else if (passedCriteria === 4) {
        strength = 'Trung bình';
        color = '#ffaa00';
        score = 3;
    } else if (passedCriteria === 5) {
        strength = 'Mạnh';
        color = '#00aa00';
        score = 4;
    }
    
    strengthText.innerHTML = `
        <div style="margin-bottom: 8px;">
            <strong>Độ mạnh: <span style="color: ${color};">${strength}</span></strong>
        </div>
        <div style="font-size: 12px; color: #666;">
            ${getPasswordDetails(criteria, password.length)}
        </div>
        <div style="margin-top: 5px;">
            ${getStrengthBar(score)}
        </div>
    `;
    
    checkPasswordMatch();
    // updateSubmitButton();
}

function checkPasswordMatch() {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const matchText = document.getElementById('password-match');
    
    if (!confirmPassword) {
        matchText.textContent = '';
        // updateSubmitButton();
        return;
    }
    
    if (password === confirmPassword) {
        matchText.innerHTML = '<span style="color: #00aa00;">✓ Mật khẩu khớp</span>';
    } else {
        matchText.innerHTML = '<span style="color: #ff4444;">✗ Mật khẩu không khớp</span>';
    }
    
    // updateSubmitButton();
}

// function updateSubmitButton() {
//     const registerBtn = document.getElementById('register-btn');
//     const isFormValid = validateUsername() && validateEmail() && checkPasswordStrength() && checkPasswordMatchValidation();
    
//     if (registerBtn) {
//         registerBtn.disabled = !isFormValid;
//         registerBtn.style.opacity = isFormValid ? '1' : '0.5';
//     }
// }

function getPasswordDetails(criteria, length) {
    const details = [];
    
    details.push(`Độ dài: ${length} ký tự ${criteria.length ? '✓' : '✗'}`);
    details.push(`Chữ thường: ${criteria.lowercase ? '✓' : '✗'}`);
    details.push(`Chữ hoa: ${criteria.uppercase ? '✓' : '✗'}`);
    details.push(`Số: ${criteria.number ? '✓' : '✗'}`);
    details.push(`Ký tự đặc biệt: ${criteria.special ? '✓' : '✗'}`);
    
    return details.join(' | ');
}

function getStrengthBar(score) {
    const bars = [];
    const colors = ['#ff4444', '#ff8800', '#ffaa00', '#00aa00'];
    
    for (let i = 0; i < 4; i++) {
        const color = i < score ? colors[i] : '#ddd';
        bars.push(`<span style="display: inline-block; width: 20px; height: 4px; background: ${color}; margin-right: 2px;"></span>`);
    }
    
    return bars.join('');
}

function generatePassword() {
    console.log("generatePassword called"); // Debug
    
    // Đảm bảo mật khẩu có đủ tất cả loại ký tự
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const numbers = '0123456789';
    const specials = '!@#$%^&*()_+-=[]{}|;:,.<>?';
    
    let password = '';
    
    // Đảm bảo có ít nhất 1 ký tự từ mỗi loại
    password += lowercase[Math.floor(Math.random() * lowercase.length)];
    password += uppercase[Math.floor(Math.random() * uppercase.length)];
    password += numbers[Math.floor(Math.random() * numbers.length)];
    password += specials[Math.floor(Math.random() * specials.length)];
    
    // Thêm các ký tự ngẫu nhiên cho đủ 12 ký tự
    const allChars = lowercase + uppercase + numbers + specials;
    for (let i = 4; i < 12; i++) {
        password += allChars[Math.floor(Math.random() * allChars.length)];
    }
    
    // Trộn ngẫu nhiên các ký tự
    password = password.split('').sort(() => Math.random() - 0.5).join('');
    
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    
    passwordInput.value = password;
    confirmPasswordInput.value = password; // Tự động điền vào ô xác nhận
    
    checkPassword(); // Gọi lại để cập nhật thông báo độ mạnh
    checkPasswordMatch(); // Kiểm tra khớp mật khẩu
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

// Thêm event listener để kiểm tra mật khẩu realtime
// Cập nhật event listeners
document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    
    if (passwordInput) {
        passwordInput.addEventListener('input', checkPassword);
    }
    
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('input', checkPasswordMatch);
    }
    
    if (usernameInput) {
    usernameInput.addEventListener('input', function () {
        validateUsername();
        // updateSubmitButton(); // <- thêm dòng này
    });
}

if (emailInput) {
    emailInput.addEventListener('input', function () {
        validateEmail();
        // updateSubmitButton(); // <- thêm dòng này
    });
}


    // Kiểm tra ban đầu
    // updateSubmitButton();
});