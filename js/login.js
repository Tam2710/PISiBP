document.getElementById('login-form').addEventListener('submit', function(event) {
  event.preventDefault();

  /*
  document.getElementById('login-form').addEventListener('submit', function(event) {
    // preventDefault() can be removed if submitting to backend
  });
  */
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  // Simple validation for login (you can add actual authentication here)
  if (email === 'test@example.com' && password === 'password123') {
    localStorage.setItem('loggedIn', 'true');
    window.location.href = 'form_creation.html';
  } else {
    document.getElementById('error-message').classList.remove('hidden');
  }

  /*
  {% if form.errors %}
    <div class="error">{{ form.errors }}</div>
  {% endif %}
  */
});