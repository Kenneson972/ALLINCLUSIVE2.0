<?php
/**
 * Générateur de Pages Villa HTML - KhanelConcept Admin
 * UTILISE LE TEMPLATE EXACT DE LA PAGE ORIGINALE
 */

require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/auth.php';  
require_once __DIR__ . '/../includes/functions.php';

// Gestion des requêtes JSON
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    
    if ($input['action'] === 'generate_single') {
        $generator = new VillaPageGenerator();
        echo json_encode($generator->generateVillaPage($input['villa_id']));
        exit;
    }
    
    if ($input['action'] === 'generate_all') {
        $generator = new VillaPageGenerator();
        echo json_encode($generator->generateAllVillas());
        exit;
    }
}

/**
 * Générateur de pages villa utilisant le template EXACT
 */
class VillaPageGenerator {
    private $pdo;
    
    public function __construct() {
        $this->pdo = new PDO(
            "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=" . DB_CHARSET,
            DB_USER, 
            DB_PASS,
            [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            ]
        );
    }
    
    /**
     * Charger le template HTML EXACT de la page originale
     */
    private function loadOriginalTemplate() {
        // Chemin vers le template original EXACT
        $template_path = __DIR__ . '/../../frontend/public/villa-villa-f3-sur-petit-macabou.html';
        
        if (file_exists($template_path)) {
            return file_get_contents($template_path);
        }
        
        // Si le fichier local n'existe pas, essayer de le télécharger
        $template_url = 'https://kenneson972.github.io/ALLINCLUSIVE2.0/frontend/public/villa-villa-f3-sur-petit-macabou.html';
        
        $context = stream_context_create([
            'http' => [
                'timeout' => 30,
                'user_agent' => 'Mozilla/5.0 (compatible; VillaGenerator/1.0)'
            ]
        ]);
        
        $template = file_get_contents($template_url, false, $context);
        
        if ($template) {
            // Sauvegarder le template localement pour les prochaines fois
            file_put_contents($template_path, $template);
            return $template;
        }
        
        throw new Exception('Impossible de charger le template original');
    }
    
    /**
     * Récupérer les données de la villa avec images
     */
    private function getVillaData($villa_id) {
        $stmt = $this->pdo->prepare("SELECT * FROM villas WHERE id = ?");
        $stmt->execute([$villa_id]);
        $villa = $stmt->fetch();
        
        if (!$villa) {
            throw new Exception("Villa avec ID $villa_id non trouvée");
        }
        
        // Récupérer les images
        $stmt = $this->pdo->prepare("
            SELECT * FROM villa_images 
            WHERE villa_id = ? 
            ORDER BY date_upload ASC
        ");
        $stmt->execute([$villa_id]);
        $images = $stmt->fetchAll();
        
        return ['villa' => $villa, 'images' => $images];
    }
    
    /**
     * Générer le HTML des images pour le carousel
     */
    private function generateCarouselHTML($images) {
        if (empty($images)) {
            return '<div class="swiper-slide">
                        <img src="assets/images/placeholders/villa-placeholder.jpg" alt="Image villa" loading="lazy">
                    </div>';
        }
        
        $carousel_html = '';
        $index = 1;
        
        foreach ($images as $image) {
            $image_path = "/admin/uploads/villas/" . $image['nom_fichier'];
            $alt_text = $image['alt_text'] ?: "Image $index";
            
            $carousel_html .= '<div class="swiper-slide swiper-slide-active" role="group" aria-label="' . $index . ' / ' . count($images) . '">';
            $carousel_html .= '<img src="' . htmlspecialchars($image_path) . '" alt="' . htmlspecialchars($alt_text) . '" loading="lazy">';
            $carousel_html .= '</div>';
            
            $index++;
        }
        
        return $carousel_html;
    }
    
    /**
     * Générer le HTML des thumbnails
     */
    private function generateThumbnailsHTML($images) {
        if (empty($images)) {
            return '<img src="assets/images/placeholders/villa-placeholder.jpg" alt="Thumbnail villa" loading="lazy">';
        }
        
        $thumbnails_html = '';
        $index = 1;
        
        foreach ($images as $image) {
            $image_path = "/admin/uploads/villas/" . $image['nom_fichier'];
            $alt_text = "Thumbnail $index";
            $active_class = $index === 1 ? ' class="active"' : '';
            
            $thumbnails_html .= '<img src="' . htmlspecialchars($image_path) . '" alt="' . htmlspecialchars($alt_text) . '"' . $active_class . ' loading="lazy" decoding="async">';
            
            $index++;
        }
        
        return $thumbnails_html;
    }
    
    /**
     * Générer le HTML des équipements
     */
    private function generateEquipementsHTML($villa) {
        $equipements_json = $villa['equipements'] ?? '[]';
        $equipements = json_decode($equipements_json, true) ?: [];
        
        // Mapping des équipements avec icônes
        $equipements_icons = [
            'climatisation' => '<i class="fas fa-snowflake text-blue-600 mr-3"></i><span>❄️ Climatisation</span>',
            'sauna' => '<i class="fas fa-spa text-blue-600 mr-3"></i><span>🧖‍♀️ Sauna</span>',
            'terrasse' => '<i class="fas fa-home text-blue-600 mr-3"></i><span>🏡 Terrasses modernes</span>',
            'canape_lit' => '<i class="fas fa-couch text-blue-600 mr-3"></i><span>🛋️ Canapé-lit</span>',
            'salle_bain' => '<i class="fas fa-bath text-blue-600 mr-3"></i><span>🛀 Salle de bain privée</span>',
            'jacuzzi' => '<i class="fas fa-hot-tub text-blue-600 mr-3"></i><span>🛁 Jacuzzi</span>',
            'wifi' => '<i class="fas fa-wifi text-blue-600 mr-3"></i><span>📶 WiFi haut débit</span>',
            'piscine' => '<i class="fas fa-swimming-pool text-blue-600 mr-3"></i><span>🏊‍♀️ Piscine</span>',
            'cuisine' => '<i class="fas fa-utensils text-blue-600 mr-3"></i><span>🍽️ Cuisine équipée</span>',
            'parking' => '<i class="fas fa-car text-blue-600 mr-3"></i><span>🚗 Parking</span>'
        ];
        
        $html = '';
        
        if (!empty($equipements)) {
            foreach ($equipements as $equipement) {
                $equipement_key = strtolower(str_replace(' ', '_', trim($equipement)));
                if (isset($equipements_icons[$equipement_key])) {
                    $html .= '<div class="amenity-item">' . $equipements_icons[$equipement_key] . '</div>';
                } else {
                    // Équipement générique
                    $html .= '<div class="amenity-item"><i class="fas fa-check text-blue-600 mr-3"></i><span>✨ ' . ucfirst($equipement) . '</span></div>';
                }
            }
        } else {
            // Équipements par défaut si aucun spécifié
            $html = '
                <div class="amenity-item"><i class="fas fa-snowflake text-blue-600 mr-3"></i><span>❄️ Climatisation</span></div>
                <div class="amenity-item"><i class="fas fa-wifi text-blue-600 mr-3"></i><span>📶 WiFi haut débit</span></div>
                <div class="amenity-item"><i class="fas fa-swimming-pool text-blue-600 mr-3"></i><span>🏊‍♀️ Piscine</span></div>
                <div class="amenity-item"><i class="fas fa-home text-blue-600 mr-3"></i><span>🏡 Terrasses modernes</span></div>
            ';
        }
        
        return $html;
    }
    
    /**
     * Générer le HTML des tarifs
     */
    private function generateTarifsHTML($villa) {
        $prix_nuit = number_format($villa['prix_nuit'], 0);
        $prix_semaine = number_format($villa['prix_nuit'] * 6.5, 0); // Réduction pour la semaine
        
        return '
            <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="font-medium">Nuit :</span>
                <span class="text-blue-600 font-bold">' . $prix_nuit . '€/nuit</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="font-medium">Semaine :</span>
                <span class="text-blue-600 font-bold">' . $prix_semaine . '€/semaine</span>
            </div>
        ';
    }
    
    /**
     * Générer une page villa complète
     */
    public function generateVillaPage($villa_id) {
        try {
            // 1. Charger le template EXACT
            $template = $this->loadOriginalTemplate();
            
            // 2. Récupérer les données de la villa
            $data = $this->getVillaData($villa_id);
            $villa = $data['villa'];
            $images = $data['images'];
            
            // 3. Préparer les remplacements - GARDER TOUTE LA STRUCTURE !
            $replacements = [
                // === TITRE ET META ===
                'Villa F3 sur Petit Macabou' => $villa['nom'],
                'Petit Macabou, Vauclin' => $villa['localisation'],
                
                // === CAPACITÉS ===
                '<div class="text-2xl font-bold text-gray-800">6</div>' => '<div class="text-2xl font-bold text-gray-800">' . $villa['capacite_max'] . '</div>',
                '<div class="text-2xl font-bold text-gray-800">3</div>' => '<div class="text-2xl font-bold text-gray-800">' . $villa['nombre_chambres'] . '</div>',
                '<div class="text-2xl font-bold text-gray-800">2</div>' => '<div class="text-2xl font-bold text-gray-800">' . $villa['nombre_salles_bain'] . '</div>',
                
                // === DESCRIPTION ===
                '**Villa F3 sur Petit Macabou - Modernité et élégance au cœur du Petit Macabou, Vauclin.**' => '**' . $villa['nom'] . ' - ' . ($villa['description'] ?: 'Villa de luxe exceptionnelle en Martinique.') . '**',
                
                // === ÉQUIPEMENTS - Remplacer toute la section ===
                '<div class="amenity-item">
                    <i class="fas fa-snowflake text-blue-600 mr-3"></i>
                    <span>❄️ Climatisation</span>
                </div>
                <div class="amenity-item">
                    <i class="fas fa-spa text-blue-600 mr-3"></i>
                    <span>🧖‍♀️ Sauna</span>
                </div>
                <div class="amenity-item">
                    <i class="fas fa-home text-blue-600 mr-3"></i>
                    <span>🏡 Terrasses modernes</span>
                </div>
                <div class="amenity-item">
                    <i class="fas fa-couch text-blue-600 mr-3"></i>
                    <span>🛋️ Canapé-lit</span>
                </div>
                <div class="amenity-item">
                    <i class="fas fa-bath text-blue-600 mr-3"></i>
                    <span>🛀 Salle de bain privée</span>
                </div>
                <div class="amenity-item">
                    <i class="fas fa-hot-tub text-blue-600 mr-3"></i>
                    <span>🛁 Jacuzzi</span>
                </div>
                <div class="amenity-item">
                    <i class="fas fa-wifi text-blue-600 mr-3"></i>
                    <span>📶 WiFi haut débit</span>
                </div>' => $this->generateEquipementsHTML($villa),
                
                // === TARIFS ===
                '<div class="flex justify-between items-center py-2 border-b border-gray-200">
                    <span class="font-medium">Grandes Vacances :</span>
                    <span class="text-blue-600 font-bold">1550€/semaine</span>
                </div>
                <div class="flex justify-between items-center py-2 border-b border-gray-200">
                    <span class="font-medium">Week-end (Ven-Dim) :</span>
                    <span class="text-blue-600 font-bold">850€ (2 nuits)</span>
                </div>' => $this->generateTarifsHTML($villa),
                
                // === CAPACITÉ MAXIMALE ===
                '6 personnes ( jusqu\'à 15 personnes en journée )' => $villa['capacite_max'] . ' personnes'
            ];
            
            // 4. Appliquer les remplacements en préservant TOUTE la structure
            $html_content = $template;
            
            foreach ($replacements as $search => $replace) {
                $html_content = str_replace($search, $replace, $html_content);
            }
            
            // 5. Remplacer les images du carousel (plus complexe)
            if (!empty($images)) {
                // Trouver et remplacer le contenu du swiper-wrapper
                $pattern = '/<div class="swiper-wrapper"[^>]*>.*?<\/div>/s';
                $carousel_content = '<div class="swiper-wrapper" id="swiper-wrapper-generated">' . $this->generateCarouselHTML($images) . '</div>';
                $html_content = preg_replace($pattern, $carousel_content, $html_content, 1);
                
                // Remplacer les thumbnails
                $pattern = '/<div class="gallery-thumbnails[^>]*>.*?<\/div>/s';
                $thumbnails_content = '<div class="gallery-thumbnails flex gap-3 overflow-x-auto p-4 bg-gray-100 rounded-b-xl">' . $this->generateThumbnailsHTML($images) . '</div>';
                $html_content = preg_replace($pattern, $thumbnails_content, $html_content, 1);
            }
            
            // 6. Sauvegarder le fichier
            $filename = 'villa-' . $villa['slug'] . '.html';
            $filepath = __DIR__ . '/../../frontend/public/' . $filename;
            
            if (!file_put_contents($filepath, $html_content)) {
                throw new Exception('Impossible de sauvegarder le fichier ' . $filename);
            }
            
            return [
                'success' => true,
                'filename' => $filename,
                'full_path' => $filepath,
                'page_url' => '/' . $filename,
                'villa_name' => $villa['nom'],
                'message' => 'Page générée avec succès'
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Générer toutes les pages villa
     */
    public function generateAllVillas() {
        try {
            $stmt = $this->pdo->query("SELECT id FROM villas ORDER BY id");
            $villa_ids = $stmt->fetchAll(PDO::FETCH_COLUMN);
            
            $results = [];
            $generated = [];
            $errors = [];
            
            foreach ($villa_ids as $villa_id) {
                $result = $this->generateVillaPage($villa_id);
                
                if ($result['success']) {
                    $generated[] = $result;
                } else {
                    $errors[] = ['villa_id' => $villa_id, 'error' => $result['error']];
                }
            }
            
            return [
                'success' => true,
                'generated' => $generated,
                'errors' => $errors,
                'total_generated' => count($generated),
                'total_errors' => count($errors)
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
}

// Interface simple pour tests
if (!isset($_POST) || empty($_POST)) {
    echo '<!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Générateur de Pages Villa</title>
        <style>
            body { font-family: Arial; padding: 2rem; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 2rem; border-radius: 10px; }
            .btn { padding: 1rem 2rem; margin: 0.5rem; border: none; border-radius: 5px; cursor: pointer; }
            .btn-primary { background: #007bff; color: white; }
            .btn-success { background: #28a745; color: white; }
            .result { margin-top: 1rem; padding: 1rem; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
            .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Générateur de Pages Villa</h1>
            <p><strong>Template utilisé :</strong> Page villa F3 originale (design EXACT)</p>
            
            <form method="POST">
                <h3>Tester une villa :</h3>
                <input type="number" name="villa_id" value="1" min="1" placeholder="ID Villa">
                <button type="submit" name="action" value="single" class="btn btn-primary">Générer Une Page</button>
            </form>
            
            <form method="POST">
                <h3>Générer toutes les villas :</h3>
                <button type="submit" name="action" value="all" class="btn btn-success">Générer Toutes les Pages</button>
            </form>
        </div>
    </body>
    </html>';
}

// Traitement des requêtes POST
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action'])) {
    $generator = new VillaPageGenerator();
    
    if ($_POST['action'] === 'single') {
        $villa_id = $_POST['villa_id'] ?? 1;
        $result = $generator->generateVillaPage($villa_id);
        
        echo '<div class="result ' . ($result['success'] ? 'success' : 'error') . '">';
        if ($result['success']) {
            echo '<h3>✅ Succès !</h3>';
            echo '<p>Page générée : <strong>' . $result['filename'] . '</strong></p>';
            echo '<p>Villa : ' . $result['villa_name'] . '</p>';
            echo '<p><a href="../../frontend/public/' . $result['filename'] . '" target="_blank">Voir la page</a></p>';
        } else {
            echo '<h3>❌ Erreur</h3>';
            echo '<p>' . $result['error'] . '</p>';
        }
        echo '</div>';
    }
    
    if ($_POST['action'] === 'all') {
        $result = $generator->generateAllVillas();
        
        echo '<div class="result ' . ($result['success'] ? 'success' : 'error') . '">';
        if ($result['success']) {
            echo '<h3>✅ Génération terminée !</h3>';
            echo '<p><strong>' . $result['total_generated'] . '</strong> pages générées</p>';
            if ($result['total_errors'] > 0) {
                echo '<p><strong>' . $result['total_errors'] . '</strong> erreurs</p>';
            }
        } else {
            echo '<h3>❌ Erreur</h3>';
            echo '<p>' . $result['error'] . '</p>';
        }
        echo '</div>';
    }
}
?>