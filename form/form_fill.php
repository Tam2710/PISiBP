<?php
// form_fill.php
 session_start();
// include '../includes/db_connect.php';

 $form_id = $_GET['form_id'] ?? '';
 $questions = get_form_questions($form_id); // Replace with actual database query
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fill Form</title>
  <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
  <div class="form-container">
    <h2>Fill Out the Form</h2>
    
    <form id="fill-form" method="POST" action="form_fill.php">
      <div id="questions-container">
        <?php

          if (!empty($questions)) {
              foreach ($questions as $question) {
                  echo "<div class='form-question'>";
                  echo "<label for='q" . $question['id'] . "'>" . htmlspecialchars($question['question_text']) . "</label>";
                  echo "<input type='text' name='question_" . $question['id'] . "' id='q" . $question['id'] . "' required>";
                  echo "</div>";
              }
          } else {
              echo "<p>No questions available for this form.</p>";
          }
          
        ?>
      </div>
      
      <button type="submit">Submit</button>
    </form>
  </div>

  <script src="../js/form_fill.js"></script>
</body>
</html>
