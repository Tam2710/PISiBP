document.addEventListener('DOMContentLoaded', () => {
  const createForm = document.getElementById('create-form');
  const addQuestionBtn = document.getElementById('add-question');

  // Attach events to a question block
  function attachEvents(block) {
    const typeSelect = block.querySelector('.question-type');
    const optionsContainer = block.querySelector('.options-container');
    const addOptionBtn = block.querySelector('.add-option');

    // Show/hide options based on question type
    typeSelect.addEventListener('change', () => {
      if (typeSelect.value === 'multiple-choice' || typeSelect.value === 'checkbox') {
        optionsContainer.style.display = 'block';
        addOptionBtn.style.display = 'inline-block';
      } else {
        optionsContainer.style.display = 'none';
        addOptionBtn.style.display = 'none';
      }
    });

    // Add new option
    addOptionBtn.addEventListener('click', () => {
      const optionDiv = document.createElement('div');
      optionDiv.className = 'option-item';

      // Text input
      const optionInput = document.createElement('input');
      optionInput.type = 'text';
      optionInput.className = 'option-input';
      optionInput.placeholder = `Option ${optionsContainer.querySelectorAll('.option-item').length + 1}`;

      // Hidden file input
      const optionImage = document.createElement('input');
      optionImage.type = 'file';
      optionImage.accept = 'image/*';
      optionImage.className = 'option-image';

      // Image icon label
      const imageLabel = document.createElement('label');
      imageLabel.className = 'option-image-label';
      imageLabel.textContent = '🖼️';
      imageLabel.title = 'Add image';
      imageLabel.addEventListener('click', () => optionImage.click());

      // Remove option button
      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'remove-btn';
      removeBtn.textContent = 'X';
      removeBtn.addEventListener('click', () => optionDiv.remove());

      optionDiv.appendChild(optionInput);
      optionDiv.appendChild(imageLabel);
      optionDiv.appendChild(optionImage);
      optionDiv.appendChild(removeBtn);

      optionsContainer.appendChild(optionDiv);
    });

    // Add delete question button if it doesn't exist
    if (!block.querySelector('.delete-question')) {
      const deleteBtn = document.createElement('button');
      deleteBtn.type = 'button';
      deleteBtn.className = 'delete-question';
      deleteBtn.textContent = 'Delete Question';
      deleteBtn.addEventListener('click', () => block.remove());
      block.appendChild(deleteBtn);
    }
  }

  // Initialize existing question blocks
  document.querySelectorAll('.question-block:not(.template)').forEach(block => {
    attachEvents(block);
  });

  // Add another question
  addQuestionBtn.addEventListener('click', () => {
    const template = document.querySelector('.question-block.template');
    const newBlock = template.cloneNode(true);
    newBlock.classList.remove('template');
    newBlock.style.display = 'block';

    // Reset fields
    const typeSelect = newBlock.querySelector('.question-type');
    typeSelect.value = 'short-answer';
    typeSelect.dispatchEvent(new Event('change')); // update add-option visibility
    newBlock.querySelector('.question-text').value = '';
    newBlock.querySelector('.question-required').checked = false;
    newBlock.querySelector('.options-container').innerHTML = '';

    createForm.insertBefore(newBlock, addQuestionBtn);
    attachEvents(newBlock);
  });

  // Submit form
  createForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    
    console.log("Submit clicked!"); // <-- check if this prints

    const formTitle = document.getElementById('form-title').value.trim();
    if (!formTitle) return alert('Please enter a form title.');

    const questionBlocks = document.querySelectorAll('.question-block:not(.template)');
    const questions = [];

    for (const block of questionBlocks) {
      const text = block.querySelector('.question-text').value.trim();
      const type = block.querySelector('.question-type').value;
      const required = block.querySelector('.question-required').checked;

      let options = [];
      if (type === 'multiple-choice' || type === 'checkbox') {
        const optionItems = block.querySelectorAll('.option-item');
        for (const item of optionItems) {
          const value = item.querySelector('.option-input').value.trim();
          const file = item.querySelector('.option-image').files[0];
          let imageData = '';
          if (file) imageData = await readFileAsync(file);
          if (value) options.push({ value, image: imageData });
        }
      }

      questions.push({ text, type, required, options });
    }

    const form = { title: formTitle, questions };
    const forms = JSON.parse(localStorage.getItem('userForms')) || [];
    forms.push(form);
    localStorage.setItem('userForms', JSON.stringify(forms));

    alert('Form saved successfully!');

    // Reset visible blocks only
    questionBlocks.forEach(block => {
      const typeSelect = block.querySelector('.question-type');
      typeSelect.value = 'short-answer';
      typeSelect.dispatchEvent(new Event('change'));
      block.querySelector('.question-text').value = '';
      block.querySelector('.question-required').checked = false;
      block.querySelector('.options-container').innerHTML = '';
    });

    document.getElementById('form-title').value = '';
  });

  // Helper to read file as Base64
  function readFileAsync(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
});
