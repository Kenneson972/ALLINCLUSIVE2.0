<?php
// Test simple du générateur
require_once __DIR__ . '/admin/includes/config.php';

// Test de chargement du template
$template_path = __DIR__ . '/frontend/public/villa-villa-f3-sur-petit-macabou.html';

if (file_exists($template_path)) {
    echo "✅ Template trouvé : " . $template_path . "\n";
    echo "📏 Taille : " . filesize($template_path) . " bytes\n";
    
    $content = file_get_contents($template_path);
    if (strpos($content, 'Villa F3 sur Petit Macabou') !== false) {
        echo "✅ Template contient le titre de référence\n";
    } else {
        echo "❌ Template ne contient pas le titre de référence\n";
    }
    
    if (strpos($content, 'swiper-wrapper') !== false) {
        echo "✅ Template contient la structure carousel\n";
    } else {
        echo "❌ Template ne contient pas la structure carousel\n";
    }
    
    if (strpos($content, 'amenity-item') !== false) {
        echo "✅ Template contient la structure équipements\n";
    } else {
        echo "❌ Template ne contient pas la structure équipements\n";
    }
    
} else {
    echo "❌ Template non trouvé : " . $template_path . "\n";
}

// Test de connexion base de données
try {
    $pdo = new PDO(
        "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET,
        DB_USER, 
        DB_PASS,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
        ]
    );
    
    echo "✅ Connexion base de données OK\n";
    
    // Test requête villas
    $stmt = $pdo->query("SELECT COUNT(*) as count FROM villas");
    $result = $stmt->fetch();
    echo "📊 Nombre de villas : " . $result['count'] . "\n";
    
    // Test requête images
    $stmt = $pdo->query("SELECT COUNT(*) as count FROM villa_images");
    $result = $stmt->fetch();
    echo "🖼️ Nombre d'images : " . $result['count'] . "\n";
    
} catch (Exception $e) {
    echo "❌ Erreur base de données : " . $e->getMessage() . "\n";
}

echo "\n🚀 Test du générateur terminé\n";
?>