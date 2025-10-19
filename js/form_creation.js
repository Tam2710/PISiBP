// form_creation.js

document.getElementById('create-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const formTitle = document.getElementById('form-title').value;
    const questionText = document.getElementById('question').value;
  
    if (formTitle.trim() === '' || questionText.trim() === '') {
      alert('Please fill in both the form title and question.');
      return;
    }
  
    const form = {
      title: formTitle,
      question: questionText
    };
  
    // Fetch existing forms from localStorage or create an empty array
    const forms = JSON.parse(localStorage.getItem('userForms')) || [];
    forms.push(form);
  
    // Save the updated forms list to localStorage
    localStorage.setItem('userForms', JSON.stringify(forms));
  
    // Clear the form fields
    document.getElementById('form-title').value = '';
    document.getElementById('question').value = '';
  
    alert('Form added successfully!');
  });
  
  // Handle form editing when editing an existing form
  window.onload = function() {
    const editForm = JSON.parse(localStorage.getItem('editForm'));
  
    if (editForm) {
      document.getElementById('form-title').value = editForm.title;
      document.getElementById('question').value = editForm.question;
  
      // Remove the edit form from localStorage after loading
      localStorage.removeItem('editForm');
    }
  };
  