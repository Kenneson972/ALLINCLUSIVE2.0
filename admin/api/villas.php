<?php
/**
 * API JSON - Villas KhanelConcept
 * Endpoint pour alimenter le frontend
 */

require_once '../includes/config.php';
require_once '../includes/functions.php';

// Headers CORS pour permettre les requêtes depuis le frontend
header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Répondre aux requêtes OPTIONS (preflight)
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

try {
    $villaManager = new VillaManager();
    
    // Paramètres de la requête
    $statut = $_GET['statut'] ?? 'disponible';
    $featured = isset($_GET['featured']) ? (bool)$_GET['featured'] : null;
    $type = $_GET['type'] ?? null;
    $limit = isset($_GET['limit']) ? (int)$_GET['limit'] : null;
    
    // Récupérer les villas
    $villas = $villaManager->getAllVillas($statut);
    
    // Filtrer par featured si demandé
    if ($featured !== null) {
        $villas = array_filter($villas, function($villa) use ($featured) {
            return (bool)$villa['featured'] === $featured;
        });
    }
    
    // Filtrer par type si demandé
    if ($type) {
        $villas = array_filter($villas, function($villa) use ($type) {
            return $villa['type'] === $type;
        });
    }
    
    // Limiter le nombre de résultats
    if ($limit && $limit > 0) {
        $villas = array_slice($villas, 0, $limit);
    }
    
    // Formater les données pour l'API
    $apiData = [];
    foreach ($villas as $villa) {
        $villaData = [
            'id' => (int)$villa['id'],
            'nom' => $villa['nom'],
            'slug' => $villa['slug'],
            'type' => $villa['type'],
            'localisation' => $villa['localisation'],
            'prix_nuit' => (float)$villa['prix_nuit'],
            'capacite_max' => (int)$villa['capacite_max'],
            'nombre_chambres' => (int)$villa['nombre_chambres'],
            'nombre_salles_bain' => (int)$villa['nombre_salles_bain'],
            'description' => $villa['description'],
            'caracteristiques' => $villa['caracteristiques'],
            'equipements' => $villa['equipements'] ? json_decode($villa['equipements'], true) : [],
            'statut' => $villa['statut'],
            'featured' => (bool)$villa['featured'],
            'image_principale' => $villa['image_principale'] ? UPLOAD_URL . $villa['image_principale'] : null,
            'url_page' => 'villa-' . $villa['slug'] . '.html',
            'created_at' => $villa['created_at'],
            'updated_at' => $villa['updated_at']
        ];
        
        // Récupérer toutes les images si demandé
        if (isset($_GET['include_images'])) {
            $images = $villaManager->getVillaImages($villa['id']);
            $villaData['images'] = array_map(function($img) {
                return [
                    'id' => (int)$img['id'],
                    'url' => UPLOAD_URL . $img['nom_fichier'],
                    'alt' => $img['alt_text'],
                    'principale' => (bool)$img['image_principale'],
                    'ordre' => (int)$img['ordre_affichage']
                ];
            }, $images);
        }
        
        $apiData[] = $villaData;
    }
    
    // Métadonnées de la réponse
    $response = [
        'success' => true,
        'data' => $apiData,
        'meta' => [
            'total' => count($apiData),
            'statut_filtre' => $statut,
            'timestamp' => date('c'),
            'version' => '1.0.0'
        ]
    ];
    
    // Si format "simple" demandé (pour compatibilité avec l'ancien code)
    if (isset($_GET['format']) && $_GET['format'] === 'simple') {
        $response = $apiData;
    }
    
    http_response_code(200);
    echo json_encode($response, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Erreur serveur',
        'message' => DEBUG_MODE ? $e->getMessage() : 'Une erreur est survenue',
        'timestamp' => date('c')
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
}
?>