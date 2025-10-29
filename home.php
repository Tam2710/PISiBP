<?php
// home.php
// include 'includes/db_connect.php';

 $forms = get_user_forms(); // Replace with actual function call
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Home - My Forms</title>
  <link rel="stylesheet" href="css/styles.css">
</head>
<body class="bg-light">
  <div class="form-container">
    <h2>Your Forms</h2>
    
    <div id="forms-list">
      <?php
        
        if (!empty($forms)) {
          foreach ($forms as $form) {
            echo "<div class='form-item'>";
            echo "<h3>" . htmlspecialchars($form['title']) . "</h3>";
            echo "<p>" . htmlspecialchars($form['description']) . "</p>";
            echo "</div>";
          }
        } else {
          echo "<p>No forms found.</p>";
        }
        
      ?>
    </div>

    <button onclick="window.location.href='form/form_creation.php'">Create New Form</button>
  </div>

  <script src="js/home.js"></script>
</body>
</html>
