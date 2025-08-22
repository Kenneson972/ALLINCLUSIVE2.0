<?php
/**
 * Test CLI simple du générateur
 */

// Configuration directe pour éviter les problèmes
define('DB_HOST', 'localhost');
define('DB_NAME', 'khanelconcept_admin');
define('DB_USER', 'root');
define('DB_PASS', '');
define('DB_CHARSET', 'utf8mb4');

// Connexion PDO simple
try {
    $pdo = new PDO("mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET, DB_USER, DB_PASS, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    echo "✅ Connexion BDD OK\n";
} catch (PDOException $e) {
    echo "❌ Erreur BDD: " . $e->getMessage() . "\n";
    exit(1);
}

// Test récupération villa
$stmt = $pdo->query("SELECT * FROM villas LIMIT 1");
$villa = $stmt->fetch();

if ($villa) {
    echo "✅ Villa trouvée: " . $villa['nom'] . "\n";
    echo "   - Slug: " . $villa['slug'] . "\n";
    echo "   - Type: " . $villa['type'] . "\n";
    echo "   - Prix: " . $villa['prix_nuit'] . "€\n\n";
    
    // Test de création de page simple
    $template = '<!DOCTYPE html>
<html lang="fr">
<head>
    <title>{{VILLA_TITRE}} - KhanelConcept</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>{{VILLA_TITRE}}</h1>
    <h2>{{VILLA_LOCALISATION}}</h2>
    <p>Type: {{VILLA_TYPE}}</p>
    <p>Prix: {{VILLA_PRIX}}€/nuit</p>
    <p>Capacité: {{VILLA_CAPACITE}} personnes</p>
    <p>{{VILLA_DESCRIPTION}}</p>
</body>
</html>';
    
    // Remplacements
    $content = str_replace([
        '{{VILLA_TITRE}}',
        '{{VILLA_LOCALISATION}}',
        '{{VILLA_TYPE}}',
        '{{VILLA_PRIX}}',
        '{{VILLA_CAPACITE}}',
        '{{VILLA_DESCRIPTION}}'
    ], [
        $villa['nom'],
        $villa['localisation'],
        $villa['type'],
        number_format($villa['prix_nuit'], 0),
        $villa['capacite_max'],
        $villa['description'] ?: 'Description à venir'
    ], $template);
    
    // Créer le fichier
    $filename = "villa-" . $villa['slug'] . ".html";
    $filepath = "/app/frontend/public/" . $filename;
    
    if (file_put_contents($filepath, $content)) {
        echo "✅ Page générée: $filename\n";
        echo "   - Taille: " . strlen($content) . " octets\n";
        echo "   - Chemin: $filepath\n";
    } else {
        echo "❌ Erreur création fichier\n";
    }
    
} else {
    echo "❌ Aucune villa trouvée\n";
}

echo "\n=== Test terminé ===\n";
?>