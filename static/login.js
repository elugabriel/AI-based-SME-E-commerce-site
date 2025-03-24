const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

loginBtn.addEventListener('click', () => {
  loginBtn.classList.add('active');
  registerBtn.classList.remove('active');
  loginForm.style.display = 'block';
  registerForm.style.display = 'none';
});

registerBtn.addEventListener('click', () => {
  registerBtn.classList.add('active');
  loginBtn.classList.remove('active');
  registerForm.style.display = 'block';
  loginForm.style.display = 'none';
});
