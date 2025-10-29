<?php
// login.php
session_start();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = $_POST['email'] ?? '';
    $password = $_POST['password'] ?? '';


    // 1. Connect to the database
    $pdo = new PDO('mysql:host=localhost;dbname=your_database', 'username', 'password');
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 2. Check if the user exists
    $stmt = $pdo->prepare('SELECT * FROM users WHERE email = :email');
    $stmt->execute(['email' => $email]);
    $user = $stmt->fetch();

    // 3. If user exists, verify the password
    if ($user && password_verify($password, $user['password'])) {
        // Set session for logged-in user
        $_SESSION['user'] = $user;
        header("Location: home.php"); // Redirect to the home page (or any other page)
        exit;
    } else {
        $error_message = 'Invalid login credentials';
    }

    // Simulating successful login without DB (for testing purposes)
    if ($email === 'test@example.com' && $password === 'password123') {
        $_SESSION['user'] = ['email' => $email]; // Store user data in session
        header("Location: home.php"); // Redirect to home page
        exit;
    } else {
        $error_message = 'Invalid login credentials';
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login</title>
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
  <div class="login-container">
    <h2>Login</h2>

    <form id="login-form" method="POST" action="login.php">
      <input type="email" name="email" id="email" placeholder="Email" required><br>
      <input type="password" name="password" id="password" placeholder="Password" required><br>
      <button type="submit">Login</button>
    </form>

    <div id="error-message" class="hidden"><?php echo isset($error_message) ? htmlspecialchars($error_message) : ''; ?></div>

    <p>Don't have an account? <a href="signup.php">Sign Up here</a></p>
  </div>

  <script src="js/login.js"></script>
</body>
</html>
