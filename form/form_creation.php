<?php
// form_creation.php
 session_start();
// include '../includes/db_connect.php';
 if ($_SERVER['REQUEST_METHOD'] === 'POST') {
     $formTitle = $_POST['form_title'] ?? '';
     $question = $_POST['question'] ?? '';
     // TODO: Save the form and question to the database
 }
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Create Form</title>
  <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
  <div class="form-container">
    <h2>Create a Form</h2>
    
    <form id="create-form" method="POST" action="form_creation.php">
      <input type="text" name="form_title" id="form-title" placeholder="Form Title" required><br>
      <textarea name="question" id="question" placeholder="Enter a question" required></textarea><br>
      <button type="submit">Add Question</button>
    </form>

    <div id="form-questions">
      <h3>Questions</h3>
      <ul id="questions-list">
        <?php

          if (!empty($questions)) {
              foreach ($questions as $q) {
                  echo "<li>" . htmlspecialchars($q) . "</li>";
              }
          } else {
              echo "<li>No questions added yet.</li>";
          }
          
        ?>
      </ul>
    </div>
  </div>

  <script src="../js/form_creation.js"></script>
</body>
</html>
