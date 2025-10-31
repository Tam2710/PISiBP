const API_URL = 'http://localhost:8000/api/';
let token = localStorage.getItem('token');

// Login
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const res = await fetch(API_URL + 'token/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });
  const data = await res.json();
  if(data.access){
    token = data.access;
    localStorage.setItem('token', token);
    alert('Logged in!');
    loadForms();
  } else {
    alert('Login failed');
  }
});

// Logout
function logout(){
  localStorage.removeItem('token');
  token = null;
  location.reload();
}

// Load forms
async function loadForms(){
  if(!token) return;
  const res = await fetch(API_URL + 'forms/', {
    headers: {'Authorization': `Bearer ${token}`}
  });
  const forms = await res.json();
  const container = document.getElementById('formsList');
  container.innerHTML = '';
  forms.forEach(f => {
    const div = document.createElement('div');
    div.innerHTML = `
      <h3>${f.name}</h3>
      <p>${f.description}</p>
      <button onclick="fillForm(${f.id})">Fill Form</button>
      <button onclick="editForm(${f.id})">Edit Form</button>
      <button onclick="viewResults(${f.id})">Results</button>
    `;
    container.appendChild(div);
  });
}

// Navigation functions (redirect to respective pages)
function fillForm(id){
  localStorage.setItem('formId', id);
  window.location.href = 'fill_form.html';
}
function editForm(id){
  localStorage.setItem('formId', id);
  window.location.href = 'form_editor.html';
}
function viewResults(id){
  localStorage.setItem('formId', id);
  window.location.href = 'results.html';
}

// Auto-load dashboard if logged in
if(token){
  loadForms();
}
