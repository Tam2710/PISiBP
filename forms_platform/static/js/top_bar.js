const API_URL = "http://127.0.0.1:8000/api/";

function updateButtons() {
  const loggedIn = !!localStorage.getItem('access');
  const loginBtn  = document.getElementById('btnLogin');
  const signupBtn = document.getElementById('btnSignup');
  const createBtn = document.getElementById('btnCreate');
  const viewBtn   = document.getElementById('btnView');
  const logoutBtn = document.getElementById('btnLogout');

  if (!loginBtn) return;  // ako je topbar slučajno nije učitan

  loginBtn.style.display  = loggedIn ? 'none' : 'inline-block';
  signupBtn.style.display = loggedIn ? 'none' : 'inline-block';
  createBtn.style.display = loggedIn ? 'inline-block' : 'none';
  viewBtn.style.display   = loggedIn ? 'inline-block' : 'none';
  logoutBtn.style.display = loggedIn ? 'inline-block' : 'none';
}

function logout() {
  localStorage.clear();

  // ako postoji renderWelcome na stranici – pozovi ga
  if (typeof renderWelcome === 'function') {
    renderWelcome();
  }

  updateButtons();

  // ako nismo na index strani, vrati nas na početnu
  if (window.location.pathname !== '/') {
    window.location.href = '/';
  }
}

function showPopup(type) {
  const popup = document.getElementById('popup');
  popup.classList.remove('hidden');
  popup.innerHTML = `
    <div class="popup-content">
      <h3>${type === 'login' ? 'Login' : 'Sign Up'}</h3>
      <input type="email" id="${type}Email" placeholder="Email" required>
      <input type="password" id="${type}Pass" placeholder="Password" required>
      <button onclick="${type === 'login' ? 'login()' : 'register()'}">
        ${type === 'login' ? 'Login' : 'Register'}
      </button>
      <button style="background:#ccc;color:black" onclick="closePopup()">Cancel</button>
    </div>
  `;
}

function closePopup() {
  document.getElementById('popup').classList.add('hidden');
}

async function register() {
  const email = document.getElementById('signupEmail').value;
  const password = document.getElementById('signupPass').value;

  const res = await fetch('http://127.0.0.1:8000/register/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email, password})
  });

  const data = await res.json();

  if (res.ok) {
    alert('✅ Registration successful!');
    closePopup();
    showPopup('login');
  } else {
    alert(data.error || '❌ Registration failed.');
  }
}

async function login() {
  const email = document.getElementById('loginEmail').value;
  const password = document.getElementById('loginPass').value;

  const res = await fetch('http://127.0.0.1:8000/login/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({email, password})
  });

  const data = await res.json();

  if (res.ok) {
    localStorage.setItem('access', data.access);
    localStorage.setItem('refresh', data.refresh);
    localStorage.setItem('user', JSON.stringify(data.user));
    closePopup();
    updateButtons();

    if (typeof renderWelcome === 'function') {
      renderWelcome();
    } else {
      // ako smo na nekoj drugoj stranici, samo osveži
      window.location.reload();
    }
  } else {
    alert(data.error || '❌ Login failed.');
  }
}

function createForm() {
  localStorage.removeItem('formId');
  localStorage.removeItem('formData');
  window.location.href = '/form_editor/';
}

function openViewForms() {
  window.location.href = '/forms/';
}

// da se dugmad odmah prilagode kad se stranica učita
document.addEventListener('DOMContentLoaded', updateButtons);