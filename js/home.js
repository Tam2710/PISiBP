window.onload = function() {
  const formsList = document.getElementById('forms-list');
  const searchBar = document.getElementById('search-bar');
  const createBtn = document.getElementById('create-form-btn');
  const loginLink = document.getElementById('login-link');

  // Fetch forms and login status from localStorage
  const forms = JSON.parse(localStorage.getItem('userForms')) || [];
  const loggedIn = localStorage.getItem('loggedIn') === 'true';

  // Toggle visibility based on login
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

    const filteredForms = forms.filter(form => form.title.toLowerCase().includes(filter.toLowerCase()));

    if (filteredForms.length === 0) {
      formsList.innerHTML = "<p>" + (forms.length === 0 ? "You haven't created any forms yet." : "No forms match your search.") + "</p>";
      return;
    }

    filteredForms.forEach((form, index) => {
      const formDiv = document.createElement('div');
      formDiv.classList.add('form-item');

      const formTitle = document.createElement('h3');
      formTitle.textContent = form.title;
      formDiv.appendChild(formTitle);

      // Edit/Delete buttons only if logged in
      if (loggedIn) {
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit';
        editButton.onclick = () => editForm(index);

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.onclick = () => deleteForm(index);

        formDiv.appendChild(editButton);
        formDiv.appendChild(deleteButton);
      }

      formsList.appendChild(formDiv);
    });
  }

  // Initial render
  renderForms();

  // Search functionality
  searchBar.addEventListener('input', function() {
    renderForms(this.value);
  });

  // Edit a form
  function editForm(index) {
    const form = forms[index];
    localStorage.setItem('editForm', JSON.stringify(form));
    window.location.href = 'form/form_creation.html';
  }

  // Delete a form
  function deleteForm(index) {
    if (!confirm('Are you sure you want to delete this form?')) return;
    forms.splice(index, 1);
    localStorage.setItem('userForms', JSON.stringify(forms));
    renderForms(searchBar.value); // Re-render with current search filter
  }
};

