<?php
/**
 * Système d'authentification - KhanelConcept Admin
 */

require_once 'config.php';

class Auth {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    /**
     * Connecter un utilisateur
     */
    public function login($email, $password) {
        try {
            $sql = "SELECT * FROM admin_users WHERE email = ? AND actif = 1";
            $stmt = $this->db->query($sql, [$email]);
            $user = $stmt->fetch();
            
            if ($user && password_verify($password, $user['password_hash'])) {
                // Mise à jour du last_login
                $updateSql = "UPDATE admin_users SET last_login = NOW() WHERE id = ?";
                $this->db->query($updateSql, [$user['id']]);
                
                // Stockage en session
                $_SESSION['admin_user'] = [
                    'id' => $user['id'],
                    'email' => $user['email'],
                    'nom' => $user['nom'],
                    'prenom' => $user['prenom'],
                    'role' => $user['role']
                ];
                
                return true;
            }
            
            return false;
            
        } catch (Exception $e) {
            error_log("Erreur login : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Déconnecter l'utilisateur
     */
    public function logout() {
        unset($_SESSION['admin_user']);
        session_destroy();
    }
    
    /**
     * Vérifier si l'utilisateur est connecté
     */
    public function isLoggedIn() {
        return isset($_SESSION['admin_user']);
    }
    
    /**
     * Obtenir l'utilisateur connecté
     */
    public function getCurrentUser() {
        return $_SESSION['admin_user'] ?? null;
    }
    
    /**
     * Vérifier le rôle de l'utilisateur
     */
    public function hasRole($role) {
        $user = $this->getCurrentUser();
        return $user && $user['role'] === $role;
    }
    
    /**
     * Vérifier si l'utilisateur est admin
     */
    public function isAdmin() {
        return $this->hasRole('admin');
    }
    
    /**
     * Créer un nouvel utilisateur admin
     */
    public function createUser($email, $password, $nom, $prenom, $role = 'manager') {
        try {
            $passwordHash = password_hash($password, PASSWORD_DEFAULT);
            
            $sql = "INSERT INTO admin_users (email, password_hash, nom, prenom, role) 
                    VALUES (?, ?, ?, ?, ?)";
            
            $this->db->query($sql, [$email, $passwordHash, $nom, $prenom, $role]);
            
            return true;
            
        } catch (Exception $e) {
            error_log("Erreur création utilisateur : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Changer le mot de passe
     */
    public function changePassword($userId, $newPassword) {
        try {
            $passwordHash = password_hash($newPassword, PASSWORD_DEFAULT);
            
            $sql = "UPDATE admin_users SET password_hash = ? WHERE id = ?";
            $this->db->query($sql, [$passwordHash, $userId]);
            
            return true;
            
        } catch (Exception $e) {
            error_log("Erreur changement mot de passe : " . $e->getMessage());
            return false;
        }
    }
}

/**
 * Middleware : Vérifier que l'utilisateur est connecté
 */
function requireAuth() {
    $auth = new Auth();
    if (!$auth->isLoggedIn()) {
        redirect('/admin/login.php', 'Vous devez être connecté pour accéder à cette page.', 'error');
    }
}

/**
 * Middleware : Vérifier que l'utilisateur est admin
 */
function requireAdmin() {
    $auth = new Auth();
    if (!$auth->isLoggedIn() || !$auth->isAdmin()) {
        redirect('/admin/login.php', 'Accès réservé aux administrateurs.', 'error');
    }
}

/**
 * Obtenir l'utilisateur connecté (fonction helper)
 */
function getCurrentUser() {
    $auth = new Auth();
    return $auth->getCurrentUser();
}

?>