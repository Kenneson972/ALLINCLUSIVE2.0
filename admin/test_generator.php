<?php
/**
 * Test du générateur de pages villa
 */

require_once 'includes/config.php';
require_once 'includes/auth.php';
require_once 'includes/functions.php';

// Désactiver l'authentification pour le test
// requireAuth();

$villaManager = new VillaManager();

// Test : récupérer une villa
echo "=== TEST GENERATEUR DE PAGES VILLA ===\n\n";

echo "1. Test connexion BDD...\n";
try {
    $villas = $villaManager->getAllVillas();
    echo "✅ Connexion BDD OK - " . count($villas) . " villas trouvées\n\n";
} catch (Exception $e) {
    echo "❌ Erreur BDD: " . $e->getMessage() . "\n";
    exit(1);
}

echo "2. Test récupération villa ID 1...\n";
$villa = $villaManager->getVillaById(1);
if ($villa) {
    echo "✅ Villa trouvée: " . $villa['nom'] . "\n";
    echo "   - Type: " . $villa['type'] . "\n";
    echo "   - Localisation: " . $villa['localisation'] . "\n";
    echo "   - Prix: " . formatPrice($villa['prix_nuit']) . "\n\n";
} else {
    echo "❌ Villa ID 1 non trouvée\n";
    exit(1);
}

echo "3. Test récupération images...\n";
$images = $villaManager->getVillaImages(1);
echo "✅ " . count($images) . " images trouvées\n\n";

echo "4. Test génération page...\n";
require_once 'villas/generer_pages.php';

$generator = new VillaPageGenerator($villaManager);
$result = $generator->generateVillaPage(1);

if ($result['success']) {
    echo "✅ Page générée avec succès !\n";
    echo "   - Fichier: " . $result['filename'] . "\n";
    echo "   - URL: " . $result['page_url'] . "\n";
    
    // Vérifier si le fichier existe
    if (file_exists($result['full_path'])) {
        echo "✅ Fichier créé: " . filesize($result['full_path']) . " octets\n";
    } else {
        echo "❌ Fichier non créé\n";
    }
} else {
    echo "❌ Erreur génération: " . $result['error'] . "\n";
}

echo "\n=== FIN DU TEST ===\n";
?>