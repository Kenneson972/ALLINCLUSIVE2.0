<?php
/**
 * Modifier une villa - KhanelConcept Admin
 * Interface centrale de gestion complète
 */

require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

// Vérifier l'authentification
requireAuth();

$villaManager = new VillaManager();
$currentUser = getCurrentUser();

// Récupérer l'ID de la villa
$villaId = isset($_GET['id']) ? (int)$_GET['id'] : 0;

if (!$villaId) {
    redirect('liste.php', 'Aucune villa spécifiée.', 'error');
}

// Récupérer la villa
$villa = $villaManager->getVillaById($villaId);

if (!$villa) {
    redirect('liste.php', 'Villa introuvable.', 'error');
}

// Récupérer les images
$images = $villaManager->getVillaImages($villaId);

// Équipements disponibles
$equipementsDisponibles = [
    'Piscine', 'WiFi', 'Climatisation', 'Jacuzzi', 'Vue mer', 'Vue montagne',
    'Terrasse', 'Jardin', 'Parking', 'Cuisine équipée', 'Barbecue', 'Lave-linge',
    'Lave-vaisselle', 'Télévision', 'Balcon', 'Proche plage', 'Calme', 'Animaux acceptés'
];

// Décoder les équipements existants
$equipementsActuels = $villa['equipements'] ? json_decode($villa['equipements'], true) : [];

$errors = [];
$formData = $villa; // Pré-remplir avec les données existantes

// Traitement du formulaire de modification
if ($_POST && isset($_POST['modifier_villa'])) {
    // Vérifier le token CSRF
    if (!validateCSRFToken($_POST['csrf_token'] ?? '')) {
        $errors[] = 'Token de sécurité invalide.';
    } else {
        // Récupérer et valider les nouvelles données
        $newData = [
            'nom' => trim($_POST['nom'] ?? ''),
            'type' => $_POST['type'] ?? '',
            'localisation' => trim($_POST['localisation'] ?? ''),
            'prix_nuit' => $_POST['prix_nuit'] ?? '',
            'capacite_max' => $_POST['capacite_max'] ?? '',
            'nombre_chambres' => $_POST['nombre_chambres'] ?? '',
            'nombre_salles_bain' => $_POST['nombre_salles_bain'] ?? '',
            'description' => trim($_POST['description'] ?? ''),
            'caracteristiques' => trim($_POST['caracteristiques'] ?? ''),
            'statut' => $_POST['statut'] ?? 'disponible',
            'featured' => isset($_POST['featured']) ? 1 : 0,
            'equipements' => $_POST['equipements'] ?? []
        ];
        
        // Générer le slug si le nom a changé
        if ($newData['nom'] !== $villa['nom']) {
            $baseSlug = generateSlug($newData['nom']);
            $newData['slug'] = $baseSlug;
            
            // Vérifier l'unicité du slug (exclure la villa actuelle)
            $counter = 1;
            while (!$villaManager->isSlugUnique($newData['slug'], $villaId)) {
                $newData['slug'] = $baseSlug . '-' . $counter;
                $counter++;
            }
        } else {
            $newData['slug'] = $villa['slug'];
        }
        
        // Validations (même que ajouter.php)
        if (empty($newData['nom'])) {
            $errors[] = 'Le nom de la villa est obligatoire.';
        } elseif (strlen($newData['nom']) < 3) {
            $errors[] = 'Le nom doit contenir au moins 3 caractères.';
        }
        
        if (empty($newData['type'])) {
            $errors[] = 'Le type de villa est obligatoire.';
        }
        
        if (empty($newData['localisation'])) {
            $errors[] = 'La localisation est obligatoire.';
        }
        
        if (empty($newData['prix_nuit']) || !is_numeric($newData['prix_nuit']) || $newData['prix_nuit'] <= 0) {
            $errors[] = 'Le prix par nuit doit être un nombre positif.';
        }
        
        if (empty($newData['capacite_max']) || !is_numeric($newData['capacite_max']) || $newData['capacite_max'] <= 0) {
            $errors[] = 'La capacité maximale doit être un nombre entier positif.';
        }
        
        if (empty($newData['nombre_chambres']) || !is_numeric($newData['nombre_chambres']) || $newData['nombre_chambres'] < 0) {
            $errors[] = 'Le nombre de chambres doit être un nombre entier positif ou nul.';
        }
        
        if (empty($newData['nombre_salles_bain']) || !is_numeric($newData['nombre_salles_bain']) || $newData['nombre_salles_bain'] < 0) {
            $errors[] = 'Le nombre de salles de bain doit être un nombre entier positif ou nul.';
        }
        
        // Si pas d'erreurs, mettre à jour
        if (empty($errors)) {
            if ($villaManager->updateVilla($villaId, $newData)) {
                redirect("modifier.php?id=$villaId", 'Villa modifiée avec succès !');
            } else {
                $errors[] = 'Erreur lors de la modification de la villa.';
            }
        } else {
            $formData = array_merge($villa, $newData); // Garder les nouvelles données en cas d'erreur
        }
    }
}

// Onglet actuel
$activeTab = $_GET['tab'] ?? 'informations';
if (!in_array($activeTab, ['informations', 'images', 'historique'])) {
    $activeTab = 'informations';
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modifier <?= sanitizeHtml($villa['nom']) ?> - KhanelConcept Admin</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="../assets/css/admin.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.css">
</head>
<body>
    <div class="admin-container">
        <!-- Sidebar -->
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
                <li><a href="../api/villas.php" target="_blank"><i class="fas fa-code"></i> API JSON</a></li>
                <li><a href="../../" target="_blank"><i class="fas fa-external-link-alt"></i> Voir Site</a></li>
                <li><a href="../logout.php"><i class="fas fa-sign-out-alt"></i> Déconnexion</a></li>
            </ul>
        </nav>
        
        <!-- Contenu principal -->
        <main class="main-content">
            <!-- Header -->
            <header class="admin-header">
                <div class="header-title">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <i class="fas fa-edit"></i>
                        <div>
                            <h2><?= sanitizeHtml($villa['nom']) ?></h2>
                            <p>
                                <span class="badge <?= 
                                    match($villa['statut']) {
                                        'disponible' => 'badge-success',
                                        'indisponible' => 'badge-danger',
                                        'maintenance' => 'badge-warning',
                                        default => 'badge-success'
                                    }
                                ?>"><?= ucfirst($villa['statut']) ?></span>
                                • <?= sanitizeHtml($villa['type']) ?>
                                • <?= formatPrice($villa['prix_nuit']) ?>/nuit
                                <?php if ($villa['featured']): ?>
                                    • <i class="fas fa-star" style="color: #ffc107;"></i> Vedette
                                <?php endif; ?>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="header-actions">
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                        <div id="save-status" class="save-status" style="color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-right: 1rem;">
                            <i class="fas fa-check-circle" style="color: #28a745;"></i> Sauvegardé
                        </div>
                        
                        <button onclick="duplicateVilla()" class="btn btn-primary btn-sm">
                            <i class="fas fa-copy"></i> Dupliquer
                        </button>
                        
                        <a href="liste.php" class="btn btn-warning btn-sm">
                            <i class="fas fa-list"></i> Retour
                        </a>
                    </div>
                </div>
            </header>
            
            <!-- Zone de contenu -->
            <div class="content-area">
                <?php displayFlashMessage(); ?>
                
                <!-- Breadcrumb -->
                <div class="breadcrumb">
                    <a href="../index.php"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
                    <i class="fas fa-chevron-right"></i>
                    <a href="liste.php"><i class="fas fa-home"></i> Villas</a>
                    <i class="fas fa-chevron-right"></i>
                    <span><?= sanitizeHtml($villa['nom']) ?></span>
                </div>
                
                <?php if (!empty($errors)): ?>
                    <div class="alert alert-danger">
                        <i class="fas fa-exclamation-circle"></i>
                        <strong>Erreurs de validation :</strong>
                        <ul style="margin: 0.5rem 0 0 0; padding-left: 1.5rem;">
                            <?php foreach ($errors as $error): ?>
                                <li><?= sanitizeHtml($error) ?></li>
                            <?php endforeach; ?>
                        </ul>
                    </div>
                <?php endif; ?>
                
                <!-- Onglets -->
                <div class="tabs-container">
                    <div class="tabs-nav">
                        <button class="tab-button <?= $activeTab === 'informations' ? 'active' : '' ?>" 
                                onclick="switchTab('informations')" data-tab="informations">
                            <i class="fas fa-info-circle"></i> Informations
                        </button>
                        <button class="tab-button <?= $activeTab === 'images' ? 'active' : '' ?>" 
                                onclick="switchTab('images')" data-tab="images">
                            <i class="fas fa-images"></i> Images
                            <span class="tab-badge"><?= count($images) ?></span>
                        </button>
                        <button class="tab-button <?= $activeTab === 'historique' ? 'active' : '' ?>" 
                                onclick="switchTab('historique')" data-tab="historique">
                            <i class="fas fa-history"></i> Historique
                        </button>
                    </div>
                    
                    <!-- Contenu des onglets -->
                    <div class="tabs-content">
                        
                        <!-- ONGLET INFORMATIONS -->
                        <div id="tab-informations" class="tab-content <?= $activeTab === 'informations' ? 'active' : '' ?>">
                            <form method="POST" action="" id="villa-form" data-validate>
                                <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                                <input type="hidden" id="villa_id" name="villa_id" value="<?= $villaId ?>">>
                                
                                <div class="glass-card">
                                    <div class="card-header">
                                        <h3 class="card-title"><i class="fas fa-info-circle"></i> Informations Générales</h3>
                                        <div style="display: flex; gap: 1rem;">
                                            <button type="submit" name="modifier_villa" class="btn btn-success">
                                                <i class="fas fa-save"></i> Sauvegarder
                                            </button>
                                            
                                            <button type="button" onclick="generateVillaPage()" class="btn btn-generate">
                                                <i class="fas fa-magic"></i> Générer Page HTML
                                            </button>
                                            
                                            <button type="button" onclick="resetForm()" class="btn btn-warning">
                                                <i class="fas fa-undo"></i> Annuler les modifications
                                            </button>
                                        </div>
                                    </div>
                                    
                                    <div class="form-grid">
                                        <div class="form-group">
                                            <label for="nom" class="form-label">
                                                <i class="fas fa-home"></i> Nom de la villa *
                                            </label>
                                            <input type="text" id="nom" name="nom" class="form-control" 
                                                   placeholder="Ex: Villa F3 sur Petit Macabou"
                                                   value="<?= sanitizeHtml($formData['nom']) ?>" 
                                                   required>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="slug" class="form-label">
                                                <i class="fas fa-link"></i> Slug (URL)
                                            </label>
                                            <input type="text" id="slug" name="slug" class="form-control" 
                                                   value="<?= sanitizeHtml($formData['slug']) ?>" 
                                                   readonly>
                                            <div class="form-help">Sera mis à jour automatiquement si vous changez le nom</div>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="type" class="form-label">
                                                <i class="fas fa-building"></i> Type de villa *
                                            </label>
                                            <select id="type" name="type" class="form-control" required>
                                                <option value="">Sélectionner un type</option>
                                                <?php foreach (['F3', 'F5', 'F6', 'F7', 'Studio', 'Appartement', 'Espace'] as $type): ?>
                                                    <option value="<?= $type ?>" <?= $formData['type'] === $type ? 'selected' : '' ?>>
                                                        <?= $type ?>
                                                    </option>
                                                <?php endforeach; ?>
                                            </select>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="localisation" class="form-label">
                                                <i class="fas fa-map-marker-alt"></i> Localisation *
                                            </label>
                                            <input type="text" id="localisation" name="localisation" class="form-control" 
                                                   placeholder="Ex: Petit Macabou, Vauclin"
                                                   value="<?= sanitizeHtml($formData['localisation']) ?>" 
                                                   required>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="prix_nuit" class="form-label">
                                                <i class="fas fa-euro-sign"></i> Prix par nuit (€) *
                                            </label>
                                            <input type="number" id="prix_nuit" name="prix_nuit" class="form-control" 
                                                   step="0.01" min="0"
                                                   value="<?= $formData['prix_nuit'] ?>" 
                                                   required>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="capacite_max" class="form-label">
                                                <i class="fas fa-users"></i> Capacité maximale *
                                            </label>
                                            <input type="number" id="capacite_max" name="capacite_max" class="form-control" 
                                                   min="1"
                                                   value="<?= $formData['capacite_max'] ?>" 
                                                   required>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="nombre_chambres" class="form-label">
                                                <i class="fas fa-bed"></i> Nombre de chambres *
                                            </label>
                                            <input type="number" id="nombre_chambres" name="nombre_chambres" class="form-control" 
                                                   min="0"
                                                   value="<?= $formData['nombre_chambres'] ?>" 
                                                   required>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label for="nombre_salles_bain" class="form-label">
                                                <i class="fas fa-bath"></i> Nombre de salles de bain *
                                            </label>
                                            <input type="number" id="nombre_salles_bain" name="nombre_salles_bain" class="form-control" 
                                                   min="0"
                                                   value="<?= $formData['nombre_salles_bain'] ?>" 
                                                   required>
                                        </div>
                                    </div>
                                </div>
                                
                                <!-- Équipements -->
                                <div class="glass-card">
                                    <div class="card-header">
                                        <h3 class="card-title"><i class="fas fa-list-check"></i> Équipements</h3>
                                    </div>
                                    
                                    <div class="equipements-grid">
                                        <?php foreach ($equipementsDisponibles as $equipement): ?>
                                            <label class="equipement-item">
                                                <input type="checkbox" name="equipements[]" value="<?= sanitizeHtml($equipement) ?>"
                                                       <?= in_array($equipement, $equipementsActuels) ? 'checked' : '' ?>>
                                                <span class="equipement-label">
                                                    <i class="fas fa-check"></i>
                                                    <?= sanitizeHtml($equipement) ?>
                                                </span>
                                            </label>
                                        <?php endforeach; ?>
                                    </div>
                                </div>
                                
                                <!-- Description -->
                                <div class="glass-card">
                                    <div class="card-header">
                                        <h3 class="card-title"><i class="fas fa-edit"></i> Description & Caractéristiques</h3>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="description" class="form-label">
                                            <i class="fas fa-align-left"></i> Description
                                        </label>
                                        <textarea id="description" name="description" class="form-control" rows="4"
                                                  placeholder="Description détaillée de la villa..."><?= sanitizeHtml($formData['description']) ?></textarea>
                                    </div>
                                    
                                    <div class="form-group">
                                        <label for="caracteristiques" class="form-label">
                                            <i class="fas fa-star"></i> Caractéristiques principales
                                        </label>
                                        <input type="text" id="caracteristiques" name="caracteristiques" class="form-control" 
                                               placeholder="Piscine, Vue mer, Terrasse, Climatisation"
                                               value="<?= sanitizeHtml($formData['caracteristiques']) ?>">
                                    </div>
                                </div>
                                
                                <!-- Configuration -->
                                <div class="glass-card">
                                    <div class="card-header">
                                        <h3 class="card-title"><i class="fas fa-cog"></i> Configuration</h3>
                                    </div>
                                    
                                    <div class="form-grid">
                                        <div class="form-group">
                                            <label for="statut" class="form-label">
                                                <i class="fas fa-toggle-on"></i> Statut
                                            </label>
                                            <select id="statut" name="statut" class="form-control">
                                                <?php foreach (['disponible', 'indisponible', 'maintenance'] as $statut): ?>
                                                    <option value="<?= $statut ?>" <?= $formData['statut'] === $statut ? 'selected' : '' ?>>
                                                        <?= ucfirst($statut) ?>
                                                    </option>
                                                <?php endforeach; ?>
                                            </select>
                                        </div>
                                        
                                        <div class="form-group">
                                            <label class="form-label">
                                                <i class="fas fa-star"></i> Options
                                            </label>
                                            <label class="checkbox-item">
                                                <input type="checkbox" name="featured" value="1" 
                                                       <?= $formData['featured'] ? 'checked' : '' ?>>
                                                <span class="checkbox-label">
                                                    <i class="fas fa-star"></i>
                                                    Villa en vedette
                                                </span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        
                        <!-- ONGLET IMAGES -->
                        <div id="tab-images" class="tab-content <?= $activeTab === 'images' ? 'active' : '' ?>">
                            
                            <!-- Upload Zone Intégrée -->
                            <div class="glass-card">
                                <div class="card-header">
                                    <h3 class="card-title"><i class="fas fa-cloud-upload-alt"></i> Upload Nouvelles Images</h3>
                                </div>
                                
                                <div id="upload-zone-integrated" class="upload-zone-small">
                                    <div class="upload-content">
                                        <i class="fas fa-plus" style="font-size: 2rem; color: rgba(255,255,255,0.6); margin-bottom: 0.5rem;"></i>
                                        <p style="color: rgba(255,255,255,0.8); margin: 0;">
                                            Glissez des images ou <strong>cliquez pour parcourir</strong>
                                        </p>
                                        <small style="color: rgba(255,255,255,0.6);">JPG, PNG, WebP • Max 5MB</small>
                                        <input type="file" id="images-file-input" multiple accept="image/*" style="display: none;">
                                    </div>
                                </div>
                                
                                <!-- Progress Upload -->
                                <div id="images-upload-progress" style="display: none; margin-top: 1rem;">
                                    <div class="progress-bar">
                                        <div id="images-progress-fill" class="progress-fill"></div>
                                    </div>
                                    <div id="images-progress-text" style="text-align: center; margin-top: 0.5rem; color: rgba(255,255,255,0.8);">0%</div>
                                </div>
                            </div>
                            
                            <!-- Galerie Images Existantes -->
                            <div class="glass-card">
                                <div class="card-header">
                                    <h3 class="card-title">
                                        <i class="fas fa-images"></i> Galerie Images
                                        <span id="images-total-count" class="tab-badge"><?= count($images) ?></span>
                                    </h3>
                                    <div style="display: flex; gap: 0.5rem;">
                                        <button onclick="selectAllImages()" class="btn btn-primary btn-sm">
                                            <i class="fas fa-check-square"></i> Tout sélectionner
                                        </button>
                                        <button onclick="deleteSelectedImages()" class="btn btn-danger btn-sm" disabled id="delete-selected-btn">
                                            <i class="fas fa-trash"></i> Supprimer sélection
                                        </button>
                                    </div>
                                </div>
                                
                                <?php if (empty($images)): ?>
                                    <div id="no-images-message" style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.7);">
                                        <i class="fas fa-images" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                                        <h3>Aucune image pour cette villa</h3>
                                        <p>Uploadez des images ci-dessus pour commencer la galerie.</p>
                                    </div>
                                <?php else: ?>
                                    <div class="images-instructions">
                                        <i class="fas fa-info-circle"></i>
                                        <strong>Instructions :</strong> Glissez les images pour réorganiser l'ordre d'affichage. L'image avec l'étoile ⭐ est l'image principale.
                                    </div>
                                    
                                    <div id="images-gallery-sortable" class="images-gallery-manager">
                                        <?php foreach ($images as $index => $image): ?>
                                            <div class="image-manager-item" data-image-id="<?= $image['id'] ?>" data-order="<?= $image['ordre_affichage'] ?>">
                                                <!-- Indicateur d'ordre -->
                                                <div class="image-order-number"><?= $index + 1 ?></div>
                                                
                                                <!-- Checkbox de sélection -->
                                                <input type="checkbox" class="image-selector" data-image-id="<?= $image['id'] ?>">
                                                
                                                <!-- Image -->
                                                <div class="image-container">
                                                    <img src="<?= UPLOAD_URL . $image['nom_fichier'] ?>" 
                                                         alt="<?= sanitizeHtml($image['alt_text']) ?>"
                                                         class="villa-image"
                                                         onclick="openImageModal('<?= UPLOAD_URL . $image['nom_fichier'] ?>', '<?= sanitizeHtml($image['alt_text']) ?>')">
                                                    
                                                    <!-- Badge image principale -->
                                                    <?php if ($image['image_principale']): ?>
                                                        <div class="main-image-badge">
                                                            <i class="fas fa-star"></i> Principale
                                                        </div>
                                                    <?php endif; ?>
                                                </div>
                                                
                                                <!-- Informations -->
                                                <div class="image-info">
                                                    <div class="image-filename"><?= sanitizeHtml($image['nom_original']) ?></div>
                                                    <div class="image-meta">
                                                        <?php if ($image['dimensions']): ?>
                                                            <?= $image['dimensions'] ?> •
                                                        <?php endif; ?>
                                                        <?php if ($image['taille_fichier']): ?>
                                                            <?= formatFileSize($image['taille_fichier']) ?>
                                                        <?php endif; ?>
                                                    </div>
                                                </div>
                                                
                                                <!-- Actions -->
                                                <div class="image-actions">
                                                    <div class="image-actions-row">
                                                        <?php if (!$image['image_principale']): ?>
                                                            <button onclick="setMainImage(<?= $image['id'] ?>)" 
                                                                    class="btn-image-action btn-primary" 
                                                                    title="Définir comme image principale">
                                                                <i class="fas fa-star"></i>
                                                            </button>
                                                        <?php endif; ?>
                                                        
                                                        <button onclick="editImageAlt(<?= $image['id'] ?>, '<?= sanitizeHtml($image['alt_text']) ?>')" 
                                                                class="btn-image-action btn-warning" 
                                                                title="Modifier le texte alternatif">
                                                            <i class="fas fa-edit"></i>
                                                        </button>
                                                        
                                                        <button onclick="deleteImage(<?= $image['id'] ?>)" 
                                                                class="btn-image-action btn-danger" 
                                                                title="Supprimer cette image">
                                                            <i class="fas fa-trash"></i>
                                                        </button>
                                                    </div>
                                                </div>
                                                
                                                <!-- Handle de drag -->
                                                <div class="drag-handle" title="Glisser pour réorganiser">
                                                    <i class="fas fa-grip-vertical"></i>
                                                </div>
                                            </div>
                                        <?php endforeach; ?>
                                    </div>
                                <?php endif; ?>
                            </div>
                        </div>
                        
                        <!-- ONGLET HISTORIQUE -->
                        <div id="tab-historique" class="tab-content <?= $activeTab === 'historique' ? 'active' : '' ?>">
                            <div class="glass-card">
                                <div class="card-header">
                                    <h3 class="card-title"><i class="fas fa-history"></i> Historique des Modifications</h3>
                                    <div class="form-help">Suivi des modifications apportées à cette villa</div>
                                </div>
                                
                                <div class="timeline">
                                    <div class="timeline-item">
                                        <div class="timeline-marker success">
                                            <i class="fas fa-plus"></i>
                                        </div>
                                        <div class="timeline-content">
                                            <div class="timeline-header">
                                                <h4>Villa créée</h4>
                                                <span class="timeline-date"><?= date('d/m/Y H:i', strtotime($villa['created_at'])) ?></span>
                                            </div>
                                            <p>Villa créée par <?= sanitizeHtml($currentUser['nom']) ?></p>
                                        </div>
                                    </div>
                                    
                                    <?php if ($villa['updated_at'] !== $villa['created_at']): ?>
                                    <div class="timeline-item">
                                        <div class="timeline-marker info">
                                            <i class="fas fa-edit"></i>
                                        </div>
                                        <div class="timeline-content">
                                            <div class="timeline-header">
                                                <h4>Dernière modification</h4>
                                                <span class="timeline-date"><?= date('d/m/Y H:i', strtotime($villa['updated_at'])) ?></span>
                                            </div>
                                            <p>Villa mise à jour</p>
                                        </div>
                                    </div>
                                    <?php endif; ?>
                                    
                                    <?php if (!empty($images)): ?>
                                    <div class="timeline-item">
                                        <div class="timeline-marker warning">
                                            <i class="fas fa-images"></i>
                                        </div>
                                        <div class="timeline-content">
                                            <div class="timeline-header">
                                                <h4>Images ajoutées</h4>
                                                <span class="timeline-date">Diverses dates</span>
                                            </div>
                                            <p><?= count($images) ?> image(s) dans la galerie</p>
                                        </div>
                                    </div>
                                    <?php endif; ?>
                                </div>
                                
                                <div style="margin-top: 2rem; padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                    <h4 style="color: white; margin-bottom: 1rem;">
                                        <i class="fas fa-chart-bar"></i> Statistiques
                                    </h4>
                                    <div class="stats-mini-grid">
                                        <div class="stat-mini">
                                            <div class="stat-mini-label">Prix/nuit</div>
                                            <div class="stat-mini-value"><?= formatPrice($villa['prix_nuit']) ?></div>
                                        </div>
                                        <div class="stat-mini">
                                            <div class="stat-mini-label">Capacité</div>
                                            <div class="stat-mini-value"><?= $villa['capacite_max'] ?> pers.</div>
                                        </div>
                                        <div class="stat-mini">
                                            <div class="stat-mini-label">Images</div>
                                            <div class="stat-mini-value"><?= count($images) ?></div>
                                        </div>
                                        <div class="stat-mini">
                                            <div class="stat-mini-label">Statut</div>
                                            <div class="stat-mini-value"><?= ucfirst($villa['statut']) ?></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script src="../assets/js/admin.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"></script>
    <script>
        // Variables globales
        const villaId = <?= $villaId ?>;
        const originalFormData = <?= json_encode($formData) ?>;
        let currentFormData = {...originalFormData};
        let hasUnsavedChanges = false;
        
        document.addEventListener('DOMContentLoaded', function() {
            setupFormChangeDetection();
            setupAutoSlugGeneration();
            setupKeyboardShortcuts();
        });
        
        // Gestion des onglets
        function switchTab(tabName) {
            // Mettre à jour l'URL sans recharger
            const url = new URL(window.location);
            url.searchParams.set('tab', tabName);
            window.history.pushState({}, '', url);
            
            // Gérer l'affichage des onglets
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
            document.getElementById(`tab-${tabName}`).classList.add('active');
            
            // Actions spécifiques par onglet
            if (tabName === 'images') {
                loadImagesTab();
            } else if (tabName === 'historique') {
                loadHistoriqueTab();
            }
        }
        
        // Détection des changements de formulaire
        function setupFormChangeDetection() {
            const form = document.getElementById('villa-form');
            
            form.addEventListener('input', function() {
                hasUnsavedChanges = true;
                updateSaveStatus('unsaved');
            });
            
            form.addEventListener('change', function() {
                hasUnsavedChanges = true;
                updateSaveStatus('unsaved');
            });
        }
        
        // Auto-génération du slug
        function setupAutoSlugGeneration() {
            const nomInput = document.getElementById('nom');
            const slugInput = document.getElementById('slug');
            const originalNom = nomInput.value;
            
            nomInput.addEventListener('input', function() {
                if (this.value !== originalNom) {
                    const slug = AdminPanel.generateSlug(this.value);
                    slugInput.value = slug;
                }
            });
        }
        
        // Raccourcis clavier
        function setupKeyboardShortcuts() {
            document.addEventListener('keydown', function(e) {
                // Ctrl+S pour sauvegarder
                if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                    e.preventDefault();
                    saveVilla();
                }
                
                // Echap pour annuler les modifications
                if (e.key === 'Escape' && hasUnsavedChanges) {
                    if (confirm('Annuler toutes les modifications non sauvegardées ?')) {
                        resetForm();
                    }
                }
            });
            
            // Avertir avant de quitter si modifications non sauvées
            window.addEventListener('beforeunload', function(e) {
                if (hasUnsavedChanges) {
                    e.preventDefault();
                    e.returnValue = 'Vous avez des modifications non sauvegardées. Êtes-vous sûr de vouloir quitter ?';
                }
            });
        }
        
        // Mise à jour du statut de sauvegarde
        function updateSaveStatus(status) {
            const statusElement = document.getElementById('save-status');
            
            switch (status) {
                case 'saved':
                    statusElement.innerHTML = '<i class="fas fa-check-circle" style="color: #28a745;"></i> Sauvegardé';
                    hasUnsavedChanges = false;
                    break;
                case 'unsaved':
                    statusElement.innerHTML = '<i class="fas fa-exclamation-circle" style="color: #ffc107;"></i> Modifications non sauvées';
                    break;
                case 'saving':
                    statusElement.innerHTML = '<i class="fas fa-spinner fa-spin" style="color: #17a2b8;"></i> Sauvegarde...';
                    break;
                case 'error':
                    statusElement.innerHTML = '<i class="fas fa-times-circle" style="color: #dc3545;"></i> Erreur de sauvegarde';
                    break;
            }
        }
        
        // Sauvegarder la villa
        function saveVilla() {
            if (!hasUnsavedChanges) {
                AdminPanel.showToast('Aucune modification à sauvegarder', 'info');
                return;
            }
            
            updateSaveStatus('saving');
            document.getElementById('villa-form').submit();
        }
        
        // Réinitialiser le formulaire
        function resetForm() {
            if (!hasUnsavedChanges || confirm('Annuler toutes les modifications non sauvegardées ?')) {
                location.reload();
            }
        }
        
        // Dupliquer la villa
        function duplicateVilla() {
            if (confirm('Créer une copie de cette villa ?')) {
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = 'dupliquer.php';
                
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'villa_id';
                input.value = villaId;
                
                const token = document.createElement('input');
                token.type = 'hidden';
                token.name = 'csrf_token';
                token.value = '<?= generateCSRFToken() ?>';
                
                form.appendChild(input);
                form.appendChild(token);
                document.body.appendChild(form);
                form.submit();
            }
        }
        
        // Chargement de l'onglet images (sera implémenté dans la suite)
        function loadImagesTab() {
            setupImageUpload();
            setupImageGallery();
        }
        
        // Configuration de l'upload intégré
        function setupImageUpload() {
            const uploadZone = document.getElementById('upload-zone-integrated');
            const fileInput = document.getElementById('images-file-input');
            
            if (!uploadZone || !fileInput) return;
            
            // Events
            uploadZone.addEventListener('click', () => fileInput.click());
            uploadZone.addEventListener('dragover', handleImageDragOver);
            uploadZone.addEventListener('dragleave', handleImageDragLeave);
            uploadZone.addEventListener('drop', handleImageDrop);
            fileInput.addEventListener('change', (e) => handleImageFiles(e.target.files));
        }
        
        // Configuration de la galerie avec drag & drop
        function setupImageGallery() {
            const gallery = document.getElementById('images-gallery-sortable');
            if (!gallery) return;
            
            // Sortable pour réorganisation
            new Sortable(gallery, {
                animation: 150,
                handle: '.drag-handle',
                onEnd: function(evt) {
                    updateImageOrder();
                }
            });
            
            // Gestion des sélections
            document.querySelectorAll('.image-selector').forEach(checkbox => {
                checkbox.addEventListener('change', updateSelectionButtons);
            });
        }
        
        function handleImageDragOver(e) {
            e.preventDefault();
            this.classList.add('dragover');
        }
        
        function handleImageDragLeave(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        }
        
        function handleImageDrop(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            handleImageFiles(e.dataTransfer.files);
        }
        
        function handleImageFiles(files) {
            const imageFiles = Array.from(files).filter(file => file.type.startsWith('image/'));
            
            if (imageFiles.length === 0) {
                AdminPanel.showToast('Aucun fichier image valide', 'error');
                return;
            }
            
            uploadImages(imageFiles);
        }
        
        async function uploadImages(files) {
            const progressContainer = document.getElementById('images-upload-progress');
            const progressFill = document.getElementById('images-progress-fill');
            const progressText = document.getElementById('images-progress-text');
            
            progressContainer.style.display = 'block';
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const progress = ((i / files.length) * 100).toFixed(0);
                
                progressFill.style.width = progress + '%';
                progressText.textContent = `Upload ${i + 1}/${files.length} - ${file.name}`;
                
                try {
                    await uploadSingleImage(file);
                    AdminPanel.showToast(`Image uploadée: ${file.name}`, 'success');
                } catch (error) {
                    AdminPanel.showToast(`Erreur upload ${file.name}: ${error}`, 'error');
                }
            }
            
            progressFill.style.width = '100%';
            progressText.textContent = 'Upload terminé !';
            
            setTimeout(() => {
                progressContainer.style.display = 'none';
                reloadImagesGallery();
            }, 2000);
        }
        
        function uploadSingleImage(file) {
            return new Promise((resolve, reject) => {
                const formData = new FormData();
                formData.append('action', 'upload_image');
                formData.append('villa_id', villaId);
                formData.append('image', file);
                formData.append('csrf_token', '<?= generateCSRFToken() ?>');
                
                fetch('actions/image_upload.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        resolve(data);
                    } else {
                        reject(data.error || 'Erreur inconnue');
                    }
                })
                .catch(error => reject(error.message || 'Erreur réseau'));
            });
        }
        
        function setMainImage(imageId) {
            if (!confirm('Définir cette image comme image principale ?')) return;
            
            fetch('actions/set_main_image.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'set_main_image',
                    villa_id: villaId,
                    image_id: imageId,
                    csrf_token: '<?= generateCSRFToken() ?>'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    AdminPanel.showToast('Image principale définie', 'success');
                    reloadImagesGallery();
                } else {
                    AdminPanel.showToast('Erreur: ' + data.error, 'error');
                }
            })
            .catch(error => AdminPanel.showToast('Erreur réseau', 'error'));
        }
        
        function deleteImage(imageId) {
            if (!confirm('Supprimer définitivement cette image ?')) return;
            
            fetch('actions/delete_image.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'delete_image',
                    image_id: imageId,
                    csrf_token: '<?= generateCSRFToken() ?>'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    AdminPanel.showToast('Image supprimée', 'success');
                    reloadImagesGallery();
                } else {
                    AdminPanel.showToast('Erreur: ' + data.error, 'error');
                }
            })
            .catch(error => AdminPanel.showToast('Erreur réseau', 'error'));
        }
        
        function editImageAlt(imageId, currentAlt) {
            const newAlt = prompt('Texte alternatif de l\'image:', currentAlt);
            if (newAlt === null) return;
            
            fetch('actions/update_image_alt.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'update_alt',
                    image_id: imageId,
                    alt_text: newAlt,
                    csrf_token: '<?= generateCSRFToken() ?>'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    AdminPanel.showToast('Texte alternatif modifié', 'success');
                    reloadImagesGallery();
                } else {
                    AdminPanel.showToast('Erreur: ' + data.error, 'error');
                }
            })
            .catch(error => AdminPanel.showToast('Erreur réseau', 'error'));
        }
        
        function updateImageOrder() {
            const items = document.querySelectorAll('.image-manager-item');
            const newOrder = Array.from(items).map((item, index) => ({
                id: parseInt(item.dataset.imageId),
                order: index + 1
            }));
            
            fetch('actions/reorder_images.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'reorder_images',
                    villa_id: villaId,
                    order: newOrder,
                    csrf_token: '<?= generateCSRFToken() ?>'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    AdminPanel.showToast('Ordre des images mis à jour', 'success');
                    // Mettre à jour les numéros d'ordre visuels
                    items.forEach((item, index) => {
                        const orderNumber = item.querySelector('.image-order-number');
                        if (orderNumber) orderNumber.textContent = index + 1;
                    });
                } else {
                    AdminPanel.showToast('Erreur: ' + data.error, 'error');
                }
            })
            .catch(error => AdminPanel.showToast('Erreur réseau', 'error'));
        }
        
        function selectAllImages() {
            const checkboxes = document.querySelectorAll('.image-selector');
            const allChecked = Array.from(checkboxes).every(cb => cb.checked);
            
            checkboxes.forEach(checkbox => {
                checkbox.checked = !allChecked;
            });
            
            updateSelectionButtons();
        }
        
        function updateSelectionButtons() {
            const checkedBoxes = document.querySelectorAll('.image-selector:checked');
            const deleteBtn = document.getElementById('delete-selected-btn');
            
            deleteBtn.disabled = checkedBoxes.length === 0;
            deleteBtn.innerHTML = checkedBoxes.length > 0 
                ? `<i class="fas fa-trash"></i> Supprimer sélection (${checkedBoxes.length})`
                : '<i class="fas fa-trash"></i> Supprimer sélection';
        }
        
        function deleteSelectedImages() {
            const checkedBoxes = document.querySelectorAll('.image-selector:checked');
            const imageIds = Array.from(checkedBoxes).map(cb => parseInt(cb.dataset.imageId));
            
            if (imageIds.length === 0) return;
            
            if (!confirm(`Supprimer définitivement ${imageIds.length} image(s) ?`)) return;
            
            fetch('actions/delete_multiple_images.php', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    action: 'delete_multiple',
                    image_ids: imageIds,
                    csrf_token: '<?= generateCSRFToken() ?>'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    AdminPanel.showToast(`${imageIds.length} image(s) supprimée(s)`, 'success');
                    reloadImagesGallery();
                } else {
                    AdminPanel.showToast('Erreur: ' + data.error, 'error');
                }
            })
            .catch(error => AdminPanel.showToast('Erreur réseau', 'error'));
        }
        
        function reloadImagesGallery() {
            // Pour éviter de recharger toute la page, on peut recharger juste l'onglet images
            setTimeout(() => {
                location.reload();
            }, 1000);
        }
        
        function openImageModal(src, alt) {
            // Créer une modal pour prévisualiser l'image en grand
            const modal = document.createElement('div');
            modal.className = 'image-preview-modal';
            modal.innerHTML = `
                <div class="modal-backdrop" onclick="this.parentElement.remove()"></div>
                <div class="modal-content">
                    <button class="modal-close" onclick="this.parentElement.parentElement.remove()">
                        <i class="fas fa-times"></i>
                    </button>
                    <img src="${src}" alt="${alt}" style="max-width: 90vw; max-height: 90vh; border-radius: 8px;">
                    <div style="text-align: center; margin-top: 1rem; color: white; font-weight: 600;">${alt}</div>
                </div>
            `;
            
            document.body.appendChild(modal);
        }
        
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        }
        
        // Chargement de l'onglet historique (sera implémenté dans la suite)
        function loadHistoriqueTab() {
            console.log('Chargement onglet historique...');
        }
    </script>
    
    <!-- Styles spécifiques pour les onglets -->
    <style>
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 2rem;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9rem;
        }
        
        .breadcrumb a {
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            transition: color 0.2s ease;
        }
        
        .breadcrumb a:hover {
            color: white;
        }
        
        .breadcrumb i {
            font-size: 0.8rem;
            opacity: 0.6;
        }
        
        .tabs-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            overflow: hidden;
        }
        
        .tabs-nav {
            display: flex;
            background: rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        }
        
        .tab-button {
            flex: 1;
            padding: 1rem 2rem;
            background: none;
            border: none;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            position: relative;
        }
        
        .tab-button:hover {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }
        
        .tab-button.active {
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border-bottom: 3px solid #28a745;
        }
        
        .tab-badge {
            background: rgba(255, 255, 255, 0.3);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: 700;
        }
        
        .tab-button.active .tab-badge {
            background: #28a745;
        }
        
        .tabs-content {
            padding: 2rem;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .save-status {
            transition: all 0.3s ease;
        }
        
        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        
        .equipements-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }
        
        .equipement-item {
            display: flex;
            align-items: center;
            cursor: pointer;
            padding: 0.75rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .equipement-item:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }
        
        .equipement-item input[type="checkbox"] {
            margin-right: 0.75rem;
            width: 18px;
            height: 18px;
        }
        
        .equipement-label {
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }
        
        .equipement-item input[type="checkbox"]:checked + .equipement-label {
            color: white;
        }
        
        .equipement-item input[type="checkbox"]:checked + .equipement-label i {
            color: #28a745;
        }
        
        .checkbox-item {
            display: flex;
            align-items: center;
            cursor: pointer;
            padding: 0.5rem 0;
        }
        
        .checkbox-item input[type="checkbox"] {
            margin-right: 0.75rem;
            width: 18px;
            height: 18px;
        }
        
        .checkbox-label {
            color: rgba(255, 255, 255, 0.9);
            font-weight: 500;
        }
        
        .form-help {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.6);
            margin-top: 0.25rem;
        }
        
        @media (max-width: 768px) {
            .tabs-nav {
                flex-direction: column;
            }
            
            .tab-button {
                justify-content: flex-start;
                padding: 1rem;
            }
            
            .tabs-content {
                padding: 1rem;
            }
            
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .equipements-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Styles pour l'onglet Images */
        .upload-zone-small {
            border: 2px dashed rgba(255, 255, 255, 0.3);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.03);
        }
        
        .upload-zone-small:hover,
        .upload-zone-small.dragover {
            border-color: rgba(255, 255, 255, 0.5);
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-2px);
        }
        
        .images-instructions {
            background: rgba(23, 162, 184, 0.15);
            border: 1px solid rgba(23, 162, 184, 0.3);
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 2rem;
            color: #17a2b8;
        }
        
        .images-gallery-manager {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }
        
        .image-manager-item {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s ease;
            position: relative;
            cursor: move;
        }
        
        .image-manager-item:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            border-color: rgba(255, 255, 255, 0.25);
        }
        
        .image-order-number {
            position: absolute;
            top: 8px;
            left: 8px;
            background: rgba(0, 0, 0, 0.8);
            color: white;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 700;
            z-index: 2;
        }
        
        .image-selector {
            position: absolute;
            top: 8px;
            right: 8px;
            z-index: 2;
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .image-container {
            position: relative;
            height: 160px;
            overflow: hidden;
        }
        
        .villa-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        
        .villa-image:hover {
            transform: scale(1.05);
        }
        
        .main-image-badge {
            position: absolute;
            top: 8px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(45deg, #ffc107, #ff8c00);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 15px;
            font-size: 0.7rem;
            font-weight: 700;
            box-shadow: 0 2px 8px rgba(255, 193, 7, 0.4);
        }
        
        .image-info {
            padding: 1rem;
        }
        
        .image-filename {
            font-weight: 600;
            color: white;
            margin-bottom: 0.25rem;
            font-size: 0.9rem;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .image-meta {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .image-actions {
            padding: 0 1rem 1rem;
        }
        
        .image-actions-row {
            display: flex;
            gap: 0.5rem;
            justify-content: center;
        }
        
        .btn-image-action {
            width: 32px;
            height: 32px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            font-size: 0.8rem;
        }
        
        .btn-image-action.btn-primary {
            background: rgba(0, 123, 255, 0.8);
            color: white;
        }
        
        .btn-image-action.btn-warning {
            background: rgba(255, 193, 7, 0.8);
            color: #333;
        }
        
        .btn-image-action.btn-danger {
            background: rgba(220, 53, 69, 0.8);
            color: white;
        }
        
        .btn-image-action:hover {
            transform: translateY(-2px);
            opacity: 0.9;
        }
        
        .drag-handle {
            position: absolute;
            bottom: 8px;
            right: 8px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 0.25rem;
            border-radius: 4px;
            cursor: grab;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .image-manager-item:hover .drag-handle {
            opacity: 1;
        }
        
        .drag-handle:active {
            cursor: grabbing;
        }
        
        /* Styles pour l'onglet Historique */
        .timeline {
            position: relative;
            padding-left: 2rem;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 1rem;
            top: 0;
            bottom: 0;
            width: 2px;
            background: rgba(255, 255, 255, 0.2);
        }
        
        .timeline-item {
            position: relative;
            margin-bottom: 2rem;
        }
        
        .timeline-marker {
            position: absolute;
            left: -1.75rem;
            width: 2.5rem;
            height: 2.5rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9rem;
        }
        
        .timeline-marker.success {
            background: #28a745;
        }
        
        .timeline-marker.info {
            background: #17a2b8;
        }
        
        .timeline-marker.warning {
            background: #ffc107;
        }
        
        .timeline-content {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 1.5rem;
        }
        
        .timeline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        
        .timeline-header h4 {
            color: white;
            margin: 0;
            font-size: 1.1rem;
        }
        
        .timeline-date {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
        }
        
        .timeline-content p {
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
        }
        
        .stats-mini-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 1rem;
        }
        
        .stat-mini {
            text-align: center;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 8px;
        }
        
        .stat-mini-label {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 0.25rem;
        }
        
        .stat-mini-value {
            font-size: 1.2rem;
            font-weight: 700;
            color: white;
        }
        
        /* Modal de prévisualisation d'image */
        .image-preview-modal {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            animation: fadeIn 0.3s ease;
        }
        
        .modal-backdrop {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
        
        .modal-content {
            position: relative;
            z-index: 1;
        }
        
        .modal-close {
            position: absolute;
            top: -50px;
            right: 0;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 1.2rem;
            transition: background 0.2s ease;
        }
        
        .modal-close:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        /* Responsive pour l'onglet images */
        @media (max-width: 768px) {
            .images-gallery-manager {
                grid-template-columns: 1fr;
            }
            
            .image-actions-row {
                justify-content: space-around;
            }
        }
    </style>
</body>
</html>