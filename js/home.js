//home.js
window.onload = function() {
  const formsList = document.getElementById('forms-list');
  const searchBar = document.getElementById('search-bar');
  const createBtn = document.getElementById('create-form-btn');
  const loginLink = document.getElementById('login-link');

  // Fetch all forms from localStorage
  const forms = JSON.parse(localStorage.getItem('userForms')) || [];
  const loggedIn = localStorage.getItem('loggedIn') === 'true';

  // Toggle create/login visibility
  if (!loggedIn) {
    createBtn.style.display = 'none';
    loginLink.style.display = 'inline-block';
  } else {
    createBtn.style.display = 'inline-block';
    loginLink.style.display = 'none';
  }

  // Render forms (filtered by search)
  function renderForms(filter = '') {
    formsList.innerHTML = '';

    const filteredForms = forms.filter(f => f.title.toLowerCase().includes(filter.toLowerCase()));

    if (filteredForms.length === 0) {
      formsList.innerHTML = `<p>${forms.length === 0 ? "No forms created yet." : "No forms match your search."}</p>`;
      return;
    }

    filteredForms.forEach((form, index) => {
      const formDiv = document.createElement('div');
      formDiv.classList.add('form-item');

      // Title clickable to fill form
      const formTitle = document.createElement('h3');
      formTitle.textContent = form.title;
      formTitle.style.cursor = 'pointer';
      formTitle.onclick = () => openForm(form);
      formDiv.appendChild(formTitle);

      // Buttons for logged-in users
      if (loggedIn) {
        const editBtn = document.createElement('button');
        editBtn.textContent = 'Edit';
        editBtn.onclick = () => editForm(index);

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = () => deleteForm(index);

        formDiv.appendChild(editBtn);
        formDiv.appendChild(deleteBtn);
      }

      formsList.appendChild(formDiv);
    });
  }

  renderForms();

  // Search functionality
  searchBar.addEventListener('input', () => renderForms(searchBar.value));

  // Open form to fill
  function openForm(form) {
    localStorage.setItem('fillForm', JSON.stringify(form));
    window.location.href = 'form/form_fill.html';
  }

  // Edit form (for logged-in users)
  function editForm(index) {
    localStorage.setItem('editForm', JSON.stringify(forms[index]));
    window.location.href = 'form/form_creation.html';
  }

  // Delete form (for logged-in users)
  function deleteForm(index) {
    if (!confirm('Are you sure you want to delete this form?')) return;
    forms.splice(index, 1);
    localStorage.setItem('userForms', JSON.stringify(forms));
    renderForms(searchBar.value);
  }
};

