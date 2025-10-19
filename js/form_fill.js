// form_fill.js

window.onload = function () {
  // Get the questions stored in localStorage (or could be fetched from a server)
  const questions = JSON.parse(localStorage.getItem('questions')) || [];

  if (questions.length === 0) {
    alert('No questions available. Please create a form first.');
    return;
  }

  const questionsContainer = document.getElementById('questions-container');

  // Dynamically create question fields
  questions.forEach((question, index) => {
    const questionDiv = document.createElement('div');
    questionDiv.classList.add('question');

    const label = document.createElement('label');
    label.textContent = question;

    const input = document.createElement('input');
    input.type = 'text';
    input.name = `question_${index}`;

    questionDiv.appendChild(label);
    questionDiv.appendChild(input);
    questionsContainer.appendChild(questionDiv);
  });

  // Handle form submission
  document.getElementById('fill-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const answers = {};
    const inputs = document.querySelectorAll('#questions-container input');

    inputs.forEach((input, index) => {
      answers[`question_${index}`] = input.value;
    });

    // You can send this data to a server or store it as needed
    console.log('Form Answers:', answers);

    alert('Form submitted successfully!');
  });
};
