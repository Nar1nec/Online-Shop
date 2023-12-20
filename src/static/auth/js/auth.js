document.addEventListener('DOMContentLoaded', function() {
    const signInBtnLink = document.querySelector('.signInBtn-link');
    const signUpBtnLink = document.querySelector('.signUpBtn-link');
    const wrapper = document.querySelector('.wrapper');

    if (signInBtnLink && signUpBtnLink && wrapper) {
        signInBtnLink.addEventListener('click', () => {
            console.log('Clicked Sign In');
            wrapper.classList.toggle('active');
            console.log(wrapper.classList.contains('active') ? 'Active' : 'Not Active');
        });

        signUpBtnLink.addEventListener('click', () => {
            console.log('Clicked Sign Up');
            wrapper.classList.toggle('active');
            console.log(wrapper.classList.contains('active') ? 'Active' : 'Not Active');
        });
    }
});

// auth_script.js

// auth_script.js

async function validatePasswords() {
    var emailInput = document.getElementsByName("email_reg")[0];
    var passwordInput = document.getElementById("password_reg");
    var confirmPasswordInput = document.getElementById("confirmPassword");
    var errorDiv = document.getElementById("passwordMatchError");
    var successDiv = document.getElementById("registrationSuccess");
    var userExistsErrorDiv = document.getElementById("userExistsError");

    // Проверка наличия введенного email и пароля
    if (!emailInput.value || !passwordInput.value || !confirmPasswordInput.value) {
        errorDiv.style.display = "block";
        errorDiv.innerText = "Please fill in all fields.";
        successDiv.style.display = "none";
        userExistsErrorDiv.style.display = "none";
        return;
    } else {
        errorDiv.style.display = "none";
    }

    // Проверка совпадения паролей
    if (passwordInput.value !== confirmPasswordInput.value) {
        errorDiv.style.display = "block";
        errorDiv.innerText = "Passwords do not match.";
        successDiv.style.display = "none";
        userExistsErrorDiv.style.display = "none";
        return;
    } else {
        errorDiv.style.display = "none";
    }

    var data = {
        "email": emailInput.value,
        "password": passwordInput.value
    };

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            // Обработка успешной регистрации
            successDiv.style.display = "block";
            successDiv.innerText = "Registration successful!";
            userExistsErrorDiv.style.display = "none";
        } else {
            const responseData = await response.json();
            if (responseData.detail === "REGISTER_USER_ALREADY_EXISTS") {
                // Обработка случая, когда пользователь уже существует
                successDiv.style.display = "none";
                userExistsErrorDiv.style.display = "block";
                userExistsErrorDiv.innerText = "User with this email already exists.";
            } else {
                // Обработка других ошибок
                console.error("Registration failed");
                // Добавим вывод сообщения об ошибке
                userExistsErrorDiv.style.display = "block";
                userExistsErrorDiv.innerText = "Registration failed. Please try again later.";
            }
        }
    } catch (error) {
        // Обработка ошибки сети или других проблем
        console.error("Network error:", error);
        // Добавим вывод сообщения об ошибке
        userExistsErrorDiv.style.display = "block";
        userExistsErrorDiv.innerText = "Network error. Please try again later.";
    }
}

async function login() {
    const username = document.getElementById("email_login").value;
    const password = document.getElementById("password_login").value;

    const data = new URLSearchParams();
    data.append('grant_type', '');
    data.append('username', username);
    data.append('password', password);
    data.append('scope', '');
    data.append('client_id', '');
    data.append('client_secret', '');

    try {
        const response = await fetch('http://127.0.0.1:8000/auth/jwt/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'accept': 'application/json',
            },
            body: data,
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Error details:', errorData);
            document.getElementById("loginErrorMessage").innerText = errorData.detail ? errorData.detail : 'Invalid email or password';
            document.getElementById("loginErrorMessage").style.display = "block";
        } else {
            // Получаем значение заголовка Location
            const redirectUrl = response.headers.get('Location');

            // Перенаправляем пользователя на целевой URL-адрес
            window.location.href = redirectUrl;
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const responseData = await response.json();
                console.log('Response data:', responseData);
            }
        }
    } catch (error) {
        // Обработка ошибок, возможно, сетевых проблем
        console.error("Network error:", error);
        document.getElementById("loginErrorMessage").innerText = 'Network error. Please try again later.';
        document.getElementById("loginErrorMessage").style.display = "block";
    }
}







