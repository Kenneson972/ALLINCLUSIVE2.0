<?php
/**
 * Configuration Base de Données - KhanelConcept Admin
 * Configuration pour hébergement O2Switch
 */

// ================================
// CONFIGURATION BASE DE DONNEES
// ================================

// Configuration pour O2Switch - À MODIFIER avec vos vraies données
define('DB_HOST', 'localhost');  // ou votre serveur MySQL O2Switch
define('DB_NAME', 'votre_nom_bdd_o2switch');  // Nom de votre BDD créée sur cPanel
define('DB_USER', 'votre_user_o2switch');     // Utilisateur BDD O2Switch  
define('DB_PASS', 'votre_password_o2switch'); // Mot de passe BDD O2Switch
define('DB_CHARSET', 'utf8mb4');

// ================================
// CONFIGURATION GENERALE
// ================================

// URLs et chemins
define('ADMIN_URL', '/admin');
define('SITE_URL', '/');
define('UPLOAD_PATH', __DIR__ . '/../uploads/villas/');
define('UPLOAD_URL', '/admin/uploads/villas/');

// Sécurité
define('SESSION_NAME', 'khanelconcept_admin');
define('CSRF_TOKEN_NAME', 'csrf_token');
define('PASSWORD_MIN_LENGTH', 8);

// Upload images
define('MAX_UPLOAD_SIZE', 5 * 1024 * 1024); // 5MB
define('ALLOWED_EXTENSIONS', ['jpg', 'jpeg', 'png', 'webp']);
define('IMAGE_MAX_WIDTH', 1920);
define('IMAGE_MAX_HEIGHT', 1080);

// ================================
// CLASSE DATABASE (PDO)
// ================================

class Database {
    private static $instance = null;
    private $connection;
    
    private function __construct() {
        try {
            $dsn = "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET;
            $options = [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false,
                PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES " . DB_CHARSET
            ];
            
            $this->connection = new PDO($dsn, DB_USER, DB_PASS, $options);
            
        } catch (PDOException $e) {
            die("Erreur de connexion à la base de données : " . $e->getMessage());
        }
    }
    
    public static function getInstance() {
        if (self::$instance === null) {
            self::$instance = new self();
        }
        return self::$instance;
    }
    
    public function getConnection() {
        return $this->connection;
    }
    
    public function query($sql, $params = []) {
        try {
            $stmt = $this->connection->prepare($sql);
            $stmt->execute($params);
            return $stmt;
        } catch (PDOException $e) {
            error_log("Database Error: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function lastInsertId() {
        return $this->connection->lastInsertId();
    }
}

// ================================
// FONCTIONS UTILITAIRES
// ================================

/**
 * Démarrer la session admin
 */
function startAdminSession() {
    if (session_status() === PHP_SESSION_NONE) {
        session_name(SESSION_NAME);
        session_start();
        
        // Sécurité session
        if (!isset($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
    }
}

/**
 * Générer un token CSRF
 */
function generateCSRFToken() {
    if (!isset($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Vérifier le token CSRF
 */
function validateCSRFToken($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

/**
 * Rediriger avec message
 */
function redirect($url, $message = null, $type = 'success') {
    if ($message) {
        $_SESSION['flash_message'] = $message;
        $_SESSION['flash_type'] = $type;
    }
    header("Location: $url");
    exit();
}

/**
 * Afficher les messages flash
 */
function displayFlashMessage() {
    if (isset($_SESSION['flash_message'])) {
        $message = $_SESSION['flash_message'];
        $type = $_SESSION['flash_type'] ?? 'success';
        unset($_SESSION['flash_message'], $_SESSION['flash_type']);
        
        $alertClass = $type === 'error' ? 'alert-danger' : 'alert-success';
        echo "<div class='alert $alertClass alert-dismissible fade show' role='alert'>
                $message
                <button type='button' class='btn-close' data-bs-dismiss='alert'></button>
              </div>";
    }
}

/**
 * Générer un slug à partir d'un nom
 */
function generateSlug($text) {
    $text = strtolower($text);
    $text = str_replace(['à', 'â', 'ä', 'ã'], 'a', $text);
    $text = str_replace(['é', 'è', 'ê', 'ë'], 'e', $text);
    $text = str_replace(['î', 'ï'], 'i', $text);
    $text = str_replace(['ô', 'ö', 'õ'], 'o', $text);
    $text = str_replace(['ù', 'û', 'ü'], 'u', $text);
    $text = str_replace(['ç'], 'c', $text);
    $text = preg_replace('/[^a-z0-9\s-]/', '', $text);
    $text = preg_replace('/[\s-]+/', '-', $text);
    $text = trim($text, '-');
    
    return $text;
}

/**
 * Sécuriser une chaîne HTML
 */
function sanitizeHtml($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

/**
 * Valider une adresse email
 */
function validateEmail($email) {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
}

/**
 * Formater le prix
 */
function formatPrice($price) {
    return number_format($price, 2, ',', ' ') . ' €';
}

// ================================
// INITIALISATION
// ================================

// Démarrer la session
startAdminSession();

// Récupérer l'instance de base de données
$db = Database::getInstance();
$pdo = $db->getConnection();

// Configuration timezone
date_default_timezone_set('America/Martinique');

// Configuration des erreurs en développement
if ($_SERVER['SERVER_NAME'] === 'localhost' || strpos($_SERVER['SERVER_NAME'], '.local') !== false) {
    error_reporting(E_ALL);
    ini_set('display_errors', 1);
    define('DEBUG_MODE', true);
} else {
    error_reporting(0);
    ini_set('display_errors', 0);
    define('DEBUG_MODE', false);
}

?>