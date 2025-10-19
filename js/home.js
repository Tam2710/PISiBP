// home.js

window.onload = function() {
  // Fetch the saved forms from localStorage
  const forms = JSON.parse(localStorage.getItem('userForms')) || [];

  const formsList = document.getElementById('forms-list');

  // Check if there are any forms
  if (forms.length === 0) {
    formsList.innerHTML = "<p>You haven't created any forms yet.</p>";
  } else {
    // Dynamically display the forms
    forms.forEach((form, index) => {
      const formDiv = document.createElement('div');
      formDiv.classList.add('form-item');
      
      const formTitle = document.createElement('h3');
      formTitle.textContent = form.title;
      
      const editButton = document.createElement('button');
      editButton.textContent = 'Edit';
      editButton.onclick = () => editForm(index);
      
      const deleteButton = document.createElement('button');
      deleteButton.textContent = 'Delete';
      deleteButton.onclick = () => deleteForm(index);
      
      formDiv.appendChild(formTitle);
      formDiv.appendChild(editButton);
      formDiv.appendChild(deleteButton);
      formsList.appendChild(formDiv);
    });
  }
};

// Edit a form by redirecting to the form creation page with the existing data
function editForm(index) {
  const forms = JSON.parse(localStorage.getItem('userForms')) || [];
  const form = forms[index];

  // Store the form data in localStorage or pass it as query params
  localStorage.setItem('editForm', JSON.stringify(form));

  // Redirect to form creation page with form data
  window.location.href = 'form_creation.html';
}

// Delete a form
function deleteForm(index) {
  const forms = JSON.parse(localStorage.getItem('userForms')) || [];

  // Remove the form from the array
  forms.splice(index, 1);

  // Save the updated array back to localStorage
  localStorage.setItem('userForms', JSON.stringify(forms));

  // Refresh the page to reflect changes
  window.location.reload();
}
