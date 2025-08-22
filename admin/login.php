<?php
/**
 * Page de connexion - KhanelConcept Admin
 */

require_once 'includes/config.php';
require_once 'includes/auth.php';

$error = '';

// Vérifier si déjà connecté
$auth = new Auth();
if ($auth->isLoggedIn()) {
    redirect('/admin/', 'Vous êtes déjà connecté.');
}

// Traitement du formulaire de connexion
if ($_POST && isset($_POST['login'])) {
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';
    $csrf_token = $_POST['csrf_token'] ?? '';
    
    // Vérifier le token CSRF
    if (!validateCSRFToken($csrf_token)) {
        $error = 'Token de sécurité invalide.';
    } 
    // Validation des champs
    elseif (empty($email) || empty($password)) {
        $error = 'Veuillez remplir tous les champs.';
    }
    // Validation email
    elseif (!validateEmail($email)) {
        $error = 'Adresse email invalide.';
    }
    // Tentative de connexion
    else {
        if ($auth->login($email, $password)) {
            redirect('/admin/', 'Connexion réussie ! Bienvenue.');
        } else {
            $error = 'Email ou mot de passe incorrect.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Connexion - KhanelConcept Admin</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="assets/css/admin.css">
</head>
<body>
    <div class="login-container">
        <div class="login-card fade-in-up">
            <div class="sidebar-logo">
                <h1><i class="fas fa-crown"></i> KhanelConcept</h1>
                <p>Admin Panel</p>
            </div>
            
            <div style="margin-top: 2rem;">
                <h2 class="login-title">Connexion</h2>
                <p class="login-subtitle">Accédez à votre espace d'administration</p>
                
                <?php if ($error): ?>
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle"></i> <?= sanitizeHtml($error) ?>
                    </div>
                <?php endif; ?>
                
                <form method="POST" action="">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    
                    <div class="form-group">
                        <label for="email" class="form-label">
                            <i class="fas fa-envelope"></i> Adresse email
                        </label>
                        <input 
                            type="email" 
                            id="email" 
                            name="email" 
                            class="form-control" 
                            placeholder="admin@khanelconcept.com"
                            value="<?= sanitizeHtml($_POST['email'] ?? '') ?>"
                            required
                            autofocus
                        >
                    </div>
                    
                    <div class="form-group">
                        <label for="password" class="form-label">
                            <i class="fas fa-lock"></i> Mot de passe
                        </label>
                        <input 
                            type="password" 
                            id="password" 
                            name="password" 
                            class="form-control" 
                            placeholder="••••••••"
                            required
                        >
                    </div>
                    
                    <button type="submit" name="login" class="btn btn-primary" style="width: 100%; justify-content: center; margin-top: 1rem;">
                        <i class="fas fa-sign-in-alt"></i> Se connecter
                    </button>
                </form>
                
                <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.15); color: rgba(255,255,255,0.7); font-size: 0.85rem;">
                    <p><strong>Compte par défaut :</strong></p>
                    <p>Email: admin@khanelconcept.com</p>
                    <p>Mot de passe: admin123</p>
                    <p style="color: #ffc107; margin-top: 0.5rem;">
                        <i class="fas fa-warning"></i> Changez ce mot de passe après la première connexion !
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Animation au focus sur les champs
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'translateY(-2px)';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'translateY(0)';
            });
        });
        
        // Animation du bouton
        document.querySelector('button[type="submit"]').addEventListener('mouseover', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        document.querySelector('button[type="submit"]').addEventListener('mouseout', function() {
            this.style.transform = 'translateY(0)';
        });
    </script>
</body>
</html>