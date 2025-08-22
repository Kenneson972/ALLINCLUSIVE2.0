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
     * Générer une page villa complète
     */
    public function generateVillaPage($villaId) {
        try {
            // 1. Récupérer les données de la villa
            $villa = $this->villaManager->getVillaById($villaId);
            if (!$villa) {
                throw new Exception('Villa introuvable');
            }
            
            // 2. Récupérer les images
            $images = $this->villaManager->getVillaImages($villaId);
            
            // 3. Préparer le contenu
            $content = $this->templateContent;
            
            // 4. Remplacer tous les placeholders
            $content = $this->replacePlaceholders($content, $villa, $images);
            
            // 5. Sauvegarder le fichier
            $filename = 'villa-' . $villa['slug'] . '.html';
            $filePath = __DIR__ . '/../../frontend/public/' . $filename;
            
            if (file_put_contents($filePath, $content)) {
                return [
                    'success' => true,
                    'filename' => $filename,
                    'path' => $filePath,
                    'url' => '/' . $filename,
                    'message' => "Page générée : $filename"
                ];
            } else {
                throw new Exception('Impossible d\'écrire le fichier');
            }
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Générer toutes les pages villas
     */
    public function generateAllVillaPages() {
        $results = [
            'success' => true,
            'generated' => [],
            'errors' => [],
            'total' => 0
        ];
        
        $villas = $this->villaManager->getAllVillas();
        $results['total'] = count($villas);
        
        foreach ($villas as $villa) {
            $result = $this->generateVillaPage($villa['id']);
            
            if ($result['success']) {
                $results['generated'][] = [
                    'villa' => $villa['nom'],
                    'filename' => $result['filename']
                ];
            } else {
                $results['errors'][] = [
                    'villa' => $villa['nom'],
                    'error' => $result['error']
                ];
                $results['success'] = false;
            }
        }
        
        return $results;
    }
    
    /**
     * Remplacer tous les placeholders dans le template
     */
    private function replacePlaceholders($content, $villa, $images) {
        // Décoder les équipements
        $equipements = $villa['equipements'] ? json_decode($villa['equipements'], true) : [];
        
        // Définir tous les remplacements
        $replacements = [
            // TITRE ET INFOS PRINCIPALES
            '{{VILLA_TITRE}}' => sanitizeHtml($villa['nom']),
            '{{VILLA_LOCALISATION}}' => sanitizeHtml($villa['localisation']),
            '{{VILLA_PRIX}}' => number_format($villa['prix_nuit'], 0, ',', ' '),
            '{{VILLA_CAPACITE}}' => $villa['capacite_max'],
            '{{VILLA_CHAMBRES}}' => $villa['nombre_chambres'],
            '{{VILLA_SALLES_BAIN}}' => $villa['nombre_salles_bain'],
            '{{VILLA_TYPE}}' => sanitizeHtml($villa['type']),
            
            // DESCRIPTIONS
            '{{VILLA_DESCRIPTION}}' => nl2br(sanitizeHtml($villa['description'])),
            '{{VILLA_CARACTERISTIQUES}}' => sanitizeHtml($villa['caracteristiques']),
            
            // ÉQUIPEMENTS
            '{{VILLA_EQUIPEMENTS}}' => $this->generateEquipementsHTML($equipements),
            '{{VILLA_EQUIPEMENTS_LIST}}' => $this->generateEquipementsListHTML($equipements),
            
            // IMAGES
            '{{IMAGES_CAROUSEL}}' => $this->generateCarouselHTML($images),
            '{{IMAGES_THUMBNAILS}}' => $this->generateThumbnailsHTML($images),
            '{{IMAGE_PRINCIPALE}}' => $this->getImagePrincipaleURL($images),
            
            // TARIFICATION
            '{{TARIFS_HTML}}' => $this->generateTarifsHTML($villa),
            '{{PRIX_FORMATEE}}' => formatPrice($villa['prix_nuit']),
            
            // META SEO
            '{{SEO_TITLE}}' => sanitizeHtml($villa['nom']) . ' - Location Villa Martinique - KhanelConcept',
            '{{SEO_DESCRIPTION}}' => $this->generateMetaDescription($villa),
            '{{SEO_KEYWORDS}}' => $this->generateMetaKeywords($villa, $equipements),
            
            // URLs ET LIENS
            '{{VILLA_SLUG}}' => $villa['slug'],
            '{{CANONICAL_URL}}' => 'https://khanelconcept.com/villa-' . $villa['slug'] . '.html',
            
            // DONNÉES STRUCTURÉES (JSON-LD)
            '{{STRUCTURED_DATA}}' => $this->generateStructuredData($villa, $images),
            
            // DATES
            '{{GENERATED_DATE}}' => date('Y-m-d H:i:s'),
            '{{YEAR}}' => date('Y')
        ];
        
        // Effectuer tous les remplacements
        foreach ($replacements as $placeholder => $value) {
            $content = str_replace($placeholder, $value, $content);
        }
        
        // Remplacements génériques pour le nom de villa (au cas où)
        $content = preg_replace('/Villa F3 sur Petit Macabou/', $villa['nom'], $content);
        $content = preg_replace('/Petit Macabou, Vauclin/', $villa['localisation'], $content);
        
        return $content;
    }
    
    /**
     * Générer le HTML des équipements avec icons
     */
    private function generateEquipementsHTML($equipements) {
        if (empty($equipements)) {
            return '<p>Équipements de base inclus</p>';
        }
        
        $icons = [
            'Piscine' => '<i class="fas fa-swimming-pool"></i>',
            'WiFi' => '<i class="fas fa-wifi"></i>',
            'Climatisation' => '<i class="fas fa-snowflake"></i>',
            'Jacuzzi' => '<i class="fas fa-hot-tub"></i>',
            'Vue mer' => '<i class="fas fa-water"></i>',
            'Vue montagne' => '<i class="fas fa-mountain"></i>',
            'Terrasse' => '<i class="fas fa-home"></i>',
            'Jardin' => '<i class="fas fa-seedling"></i>',
            'Parking' => '<i class="fas fa-car"></i>',
            'Cuisine équipée' => '<i class="fas fa-utensils"></i>',
            'Barbecue' => '<i class="fas fa-fire"></i>',
            'Lave-linge' => '<i class="fas fa-tshirt"></i>',
            'Lave-vaisselle' => '<i class="fas fa-bath"></i>',
            'Télévision' => '<i class="fas fa-tv"></i>',
            'Balcon' => '<i class="fas fa-building"></i>',
            'Proche plage' => '<i class="fas fa-umbrella-beach"></i>',
            'Calme' => '<i class="fas fa-leaf"></i>',
            'Animaux acceptés' => '<i class="fas fa-paw"></i>'
        ];
        
        $html = '<div class="equipements-grid">';
        foreach ($equipements as $equipement) {
            $icon = $icons[$equipement] ?? '<i class="fas fa-check"></i>';
            $html .= '<div class="equipement-item">' . $icon . ' ' . sanitizeHtml($equipement) . '</div>';
        }
        $html .= '</div>';
        
        return $html;
    }
    
    /**
     * Générer liste des équipements simple
     */
    private function generateEquipementsListHTML($equipements) {
        if (empty($equipements)) {
            return '<li>Équipements standards</li>';
        }
        
        $html = '';
        foreach ($equipements as $equipement) {
            $html .= '<li>' . sanitizeHtml($equipement) . '</li>';
        }
        
        return $html;
    }
    
    /**
     * Générer le carousel d'images
     */
    private function generateCarouselHTML($images) {
        if (empty($images)) {
            return '<div class="no-images"><i class="fas fa-image"></i> Images bientôt disponibles</div>';
        }
        
        $html = '<div class="villa-images-carousel" id="villaCarousel">';
        $html .= '<div class="main-image-container">';
        
        // Image principale (première image ou celle marquée comme principale)
        $mainImage = $this->getMainImage($images);
        $html .= '<img src="' . UPLOAD_URL . $mainImage['nom_fichier'] . '" alt="' . sanitizeHtml($mainImage['alt_text']) . '" class="main-villa-image" id="mainImage">';
        
        $html .= '</div>';
        $html .= '<div class="thumbnails-container">';
        
        foreach ($images as $index => $image) {
            $activeClass = $index === 0 ? ' active' : '';
            $html .= '<img src="' . UPLOAD_URL . $image['nom_fichier'] . '" ';
            $html .= 'alt="' . sanitizeHtml($image['alt_text']) . '" ';
            $html .= 'class="thumbnail' . $activeClass . '" ';
            $html .= 'onclick="changeMainImage(\'' . UPLOAD_URL . $image['nom_fichier'] . '\', this)">';
        }
        
        $html .= '</div></div>';
        
        return $html;
    }
    
    /**
     * Générer les thumbnails
     */
    private function generateThumbnailsHTML($images) {
        if (empty($images)) {
            return '';
        }
        
        $html = '<div class="villa-thumbnails">';
        foreach ($images as $image) {
            $html .= '<div class="thumbnail-item">';
            $html .= '<img src="' . UPLOAD_URL . $image['nom_fichier'] . '" alt="' . sanitizeHtml($image['alt_text']) . '">';
            $html .= '</div>';
        }
        $html .= '</div>';
        
        return $html;
    }
    
    /**
     * Obtenir l'URL de l'image principale
     */
    private function getImagePrincipaleURL($images) {
        $mainImage = $this->getMainImage($images);
        return $mainImage ? UPLOAD_URL . $mainImage['nom_fichier'] : '';
    }
    
    /**
     * Obtenir l'image principale
     */
    private function getMainImage($images) {
        if (empty($images)) return null;
        
        // Chercher l'image marquée comme principale
        foreach ($images as $image) {
            if ($image['image_principale']) {
                return $image;
            }
        }
        
        // Si aucune image principale, retourner la première
        return $images[0];
    }
    
    /**
     * Générer le HTML des tarifs
     */
    private function generateTarifsHTML($villa) {
        $prix = $villa['prix_nuit'];
        
        $html = '<div class="tarifs-container">';
        $html .= '<div class="tarif-principal">';
        $html .= '<span class="prix-amount">' . number_format($prix, 0, ',', ' ') . '€</span>';
        $html .= '<span class="prix-period">/nuit</span>';
        $html .= '</div>';
        
        // Tarifs dégressifs sugérés
        if ($prix > 500) {
            $prixSemaine = $prix * 6; // Économie d'1 nuit sur 7
            $prixMois = $prix * 25; // Économie sur 1 mois
            
            $html .= '<div class="tarifs-degressifs">';
            $html .= '<div class="tarif-option">';
            $html .= '<span class="tarif-duree">Semaine :</span>';
            $html .= '<span class="tarif-prix">' . number_format($prixSemaine, 0, ',', ' ') . '€</span>';
            $html .= '</div>';
            $html .= '<div class="tarif-option">';
            $html .= '<span class="tarif-duree">Mois :</span>';
            $html .= '<span class="tarif-prix">' . number_format($prixMois, 0, ',', ' ') . '€</span>';
            $html .= '</div>';
            $html .= '</div>';
        }
        
        $html .= '</div>';
        
        return $html;
    }
    
    /**
     * Générer la meta description
     */
    private function generateMetaDescription($villa) {
        $description = $villa['description'] ?: 
            "Location villa {$villa['type']} {$villa['localisation']} - {$villa['capacite_max']} personnes - {$villa['nombre_chambres']} chambres";
        
        return sanitizeHtml(substr($description, 0, 155));
    }
    
    /**
     * Générer les mots-clés meta
     */
    private function generateMetaKeywords($villa, $equipements) {
        $keywords = [
            'location villa martinique',
            'villa ' . strtolower($villa['localisation']),
            'location ' . strtolower($villa['type']),
            'villa ' . $villa['capacite_max'] . ' personnes',
            'KhanelConcept'
        ];
        
        // Ajouter les équipements comme mots-clés
        foreach ($equipements as $equipement) {
            $keywords[] = strtolower($equipement);
        }
        
        return implode(', ', array_unique($keywords));
    }
    
    /**
     * Générer les données structurées JSON-LD
     */
    private function generateStructuredData($villa, $images) {
        $mainImage = $this->getMainImage($images);
        $imageUrl = $mainImage ? 'https://khanelconcept.com' . UPLOAD_URL . $mainImage['nom_fichier'] : '';
        
        $structuredData = [
            '@context' => 'https://schema.org',
            '@type' => 'Accommodation',
            'name' => $villa['nom'],
            'description' => $villa['description'],
            'url' => 'https://khanelconcept.com/villa-' . $villa['slug'] . '.html',
            'image' => $imageUrl,
            'address' => [
                '@type' => 'PostalAddress',
                'addressLocality' => $villa['localisation'],
                'addressCountry' => 'MQ'
            ],
            'geo' => [
                '@type' => 'GeoCoordinates',
                'latitude' => '14.6415', // Coordonnées génériques Martinique
                'longitude' => '-61.0242'
            ],
            'occupancy' => [
                '@type' => 'QuantitativeValue',
                'maxValue' => $villa['capacite_max']
            ],
            'numberOfRooms' => $villa['nombre_chambres'],
            'priceRange' => formatPrice($villa['prix_nuit']) . ' par nuit',
            'provider' => [
                '@type' => 'Organization',
                'name' => 'KhanelConcept',
                'url' => 'https://khanelconcept.com'
            ]
        ];
        
        return '<script type="application/ld+json">' . json_encode($structuredData, JSON_PRETTY_PRINT) . '</script>';
    }
    
    /**
     * Template par défaut si aucun fichier trouvé
     */
    private function getDefaultTemplate() {
        return '<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{SEO_TITLE}}</title>
    <meta name="description" content="{{SEO_DESCRIPTION}}">
    <meta name="keywords" content="{{SEO_KEYWORDS}}">
    <link rel="canonical" href="{{CANONICAL_URL}}">
    {{STRUCTURED_DATA}}
    
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .villa-header { text-align: center; margin-bottom: 30px; }
        .villa-title { color: #333; font-size: 2rem; margin-bottom: 10px; }
        .villa-location { color: #666; font-size: 1.1rem; }
        .villa-images { margin: 30px 0; }
        .villa-info { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin: 30px 0; }
        .info-section h3 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 5px; }
        .equipements-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; }
        .equipement-item { padding: 8px; background: #f8f9fa; border-radius: 4px; }
        .price-section { background: #007bff; color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0; }
        .price-amount { font-size: 2rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <header class="villa-header">
            <h1 class="villa-title">{{VILLA_TITRE}}</h1>
            <p class="villa-location">{{VILLA_LOCALISATION}} • {{VILLA_TYPE}} • {{VILLA_CAPACITE}} personnes</p>
        </header>
        
        <section class="villa-images">
            {{IMAGES_CAROUSEL}}
        </section>
        
        <section class="villa-info">
            <div class="info-section">
                <h3>Description</h3>
                <p>{{VILLA_DESCRIPTION}}</p>
                
                <h3>Caractéristiques</h3>
                <ul>
                    <li>{{VILLA_CHAMBRES}} chambre(s)</li>
                    <li>{{VILLA_SALLES_BAIN}} salle(s) de bain</li>
                    <li>Capacité : {{VILLA_CAPACITE}} personnes</li>
                </ul>
            </div>
            
            <div class="info-section">
                <h3>Équipements</h3>
                {{VILLA_EQUIPEMENTS}}
            </div>
        </section>
        
        <section class="price-section">
            <div class="price-amount">{{VILLA_PRIX}}€</div>
            <div>par nuit</div>
        </section>
        
        <footer style="text-align: center; margin-top: 50px; color: #666;">
            <p>Page générée automatiquement le {{GENERATED_DATE}} par KhanelConcept Admin</p>
        </footer>
    </div>
</body>
</html>';
    }
}

// Traitement des requêtes AJAX
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    header('Content-Type: application/json');
    
    $input = json_decode(file_get_contents('php://input'), true);
    $action = $input['action'] ?? '';
    
    $generator = new VillaPageGenerator($villaManager);
    
    switch ($action) {
        case 'generate_single':
            $villaId = (int)($input['villa_id'] ?? 0);
            if ($villaId) {
                $result = $generator->generateVillaPage($villaId);
                echo json_encode($result);
            } else {
                echo json_encode(['success' => false, 'error' => 'ID villa manquant']);
            }
            break;
            
        case 'generate_all':
            $result = $generator->generateAllVillaPages();
            echo json_encode($result);
            break;
            
        default:
            echo json_encode(['success' => false, 'error' => 'Action inconnue']);
            break;
    }
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Générateur de Pages Villa - KhanelConcept Admin</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="../assets/css/admin.css">
</head>
<body>
    <div class="admin-container">
        <nav class="sidebar">
            <div class="sidebar-logo">
                <h1><i class="fas fa-crown"></i> KhanelConcept</h1>
                <p>Administration</p>
            </div>
            
            <ul class="sidebar-nav">
                <li><a href="../index.php"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li><a href="liste.php"><i class="fas fa-home"></i> Villas</a></li>
                <li><a href="ajouter.php"><i class="fas fa-plus"></i> Ajouter Villa</a></li>
                <li><a href="../images/galerie.php"><i class="fas fa-images"></i> Galerie</a></li>
                <li><a href="generer_pages.php" class="active"><i class="fas fa-code"></i> Générateur Pages</a></li>
                <li><a href="../api/villas.php" target="_blank"><i class="fas fa-code"></i> API JSON</a></li>
                <li><a href="../../" target="_blank"><i class="fas fa-external-link-alt"></i> Voir Site</a></li>
                <li><a href="../logout.php"><i class="fas fa-sign-out-alt"></i> Déconnexion</a></li>
            </ul>
        </nav>
        
        <main class="main-content">
            <header class="admin-header">
                <div class="header-title">
                    <h2><i class="fas fa-code"></i> Générateur de Pages Villa</h2>
                    <p>Créez automatiquement les pages HTML de vos villas</p>
                </div>
            </header>
            
            <div class="content-area">
                <?php displayFlashMessage(); ?>
                
                <div class="glass-card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-magic"></i> Génération Automatique</h3>
                    </div>
                    
                    <div style="text-align: center; padding: 2rem;">
                        <button onclick="generateAllPages()" class="btn btn-success" style="font-size: 1.2rem; padding: 1rem 2rem;">
                            <i class="fas fa-wand-magic-sparkles"></i> Générer Toutes les Pages Villa
                        </button>
                        
                        <p style="margin-top: 1rem; color: rgba(255,255,255,0.8);">
                            Cette action va créer/mettre à jour toutes les pages villa HTML avec les dernières données.
                        </p>
                    </div>
                    
                    <div id="generation-progress" style="display: none; margin-top: 2rem;">
                        <div class="progress-bar">
                            <div id="progress-fill" class="progress-fill"></div>
                        </div>
                        <div id="progress-text" style="text-align: center; margin-top: 1rem; color: white;"></div>
                    </div>
                    
                    <div id="generation-results" style="display: none; margin-top: 2rem;">
                        <!-- Résultats apparaîtront ici -->
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script src="../assets/js/admin.js"></script>
    <script>
        async function generateAllPages() {
            const progressContainer = document.getElementById('generation-progress');
            const progressFill = document.getElementById('progress-fill');
            const progressText = document.getElementById('progress-text');
            const resultsContainer = document.getElementById('generation-results');
            
            // Afficher le progress
            progressContainer.style.display = 'block';
            resultsContainer.style.display = 'none';
            progressFill.style.width = '0%';
            progressText.textContent = 'Initialisation de la génération...';
            
            try {
                // Simulation du progrès
                progressFill.style.width = '20%';
                progressText.textContent = 'Récupération des villas...';
                
                const response = await fetch('/admin/villas/generer_pages.php', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        action: 'generate_all'
                    })
                });
                
                progressFill.style.width = '80%';
                progressText.textContent = 'Génération des pages en cours...';
                
                const result = await response.json();
                
                progressFill.style.width = '100%';
                progressText.textContent = 'Génération terminée !';
                
                // Afficher les résultats
                setTimeout(() => {
                    displayResults(result);
                    progressContainer.style.display = 'none';
                }, 1000);
                
            } catch (error) {
                progressText.textContent = 'Erreur lors de la génération';
                progressFill.style.width = '100%';
                progressFill.style.background = '#dc3545';
                console.error('Erreur:', error);
            }
        }
        
        function displayResults(result) {
            const resultsContainer = document.getElementById('generation-results');
            
            let html = '<div class="generation-summary">';
            
            if (result.success) {
                html += '<div class="alert alert-success">';
                html += '<i class="fas fa-check-circle"></i> ';
                html += `<strong>Génération réussie !</strong> ${result.generated.length}/${result.total} pages créées.`;
                html += '</div>';
                
                if (result.generated.length > 0) {
                    html += '<h4 style="color: white; margin: 2rem 0 1rem;">Pages générées :</h4>';
                    html += '<div class="generated-pages-list">';
                    
                    result.generated.forEach(item => {
                        html += '<div class="generated-page-item">';
                        html += `<i class="fas fa-file-code"></i> ${item.villa}`;
                        html += `<a href="../../${item.filename}" target="_blank" class="btn btn-primary btn-sm">Voir</a>`;
                        html += '</div>';
                    });
                    
                    html += '</div>';
                }
            } else {
                html += '<div class="alert alert-danger">';
                html += '<i class="fas fa-exclamation-circle"></i> ';
                html += '<strong>Erreurs détectées</strong>';
                html += '</div>';
            }
            
            if (result.errors && result.errors.length > 0) {
                html += '<h4 style="color: #dc3545; margin: 2rem 0 1rem;">Erreurs :</h4>';
                html += '<div class="error-pages-list">';
                
                result.errors.forEach(item => {
                    html += '<div class="error-page-item">';
                    html += `<i class="fas fa-exclamation-triangle"></i> ${item.villa} : ${item.error}`;
                    html += '</div>';
                });
                
                html += '</div>';
            }
            
            html += '</div>';
            
            resultsContainer.innerHTML = html;
            resultsContainer.style.display = 'block';
        }
    </script>
    
    <style>
        .generation-summary {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 1.5rem;
        }
        
        .generated-pages-list,
        .error-pages-list {
            display: grid;
            gap: 0.5rem;
        }
        
        .generated-page-item,
        .error-page-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 4px;
            color: white;
        }
        
        .error-page-item {
            color: #dc3545;
        }
        
        .generated-page-item i,
        .error-page-item i {
            margin-right: 0.5rem;
        }
    </style>
</body>
</html>