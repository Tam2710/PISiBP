<?php
// sign_up.php
session_start();


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';
    
    // Simple validation for email and password
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error_message = 'Invalid email format';
    } elseif (strlen($password) < 6) {
        $error_message = 'Password should be at least 6 characters long';
    } else {
        
        // 1. Connect to the database
        $pdo = new PDO('mysql:host=localhost;dbname=your_database', 'username', 'password');
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // 2. Check if the user already exists
        $stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
        $stmt->execute(['email' => $email]);
        $user = $stmt->fetch();
        
        if ($user) {
            $error_message = 'User already exists';
        } else {
            // 3. Hash the password for security
            $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

            // 4. Insert the new user into the database
            $stmt = $pdo->prepare('INSERT INTO users (email, password) VALUES (:email, :password)');
            $stmt->execute(['email' => $email, 'password' => $hashedPassword]);

            // 5. Redirect to login page after successful registration
            header("Location: login.php");
            exit;
        }
        
        // Simulating successful registration without DB
        $_SESSION['user'] = ['email' => $email];
        header("Location: login.php"); // Redirect to login page after successful registration
        exit;
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign Up</title>
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
  <div class="login-container">
    <h2>Create an Account</h2>

    <form id="signup-form" method="POST" action="signup.php">
      <input type="email" name="email" id="email" placeholder="Email" required><br>
      <input type="password" name="password" id="password" placeholder="Password" required><br>
      <button type="submit">Sign Up</button>
    </form>

    <?php if (isset($error_message)): ?>
        <div class="error"><?php echo htmlspecialchars($error_message); ?></div>
    <?php endif; ?>

    <p>Already have an account? <a href="login.php">Login here</a></p>
  </div>
</body>
</html>
