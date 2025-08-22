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
                                
                                <div class="glass-card">
                                    <div class="card-header">
                                        <h3 class="card-title"><i class="fas fa-info-circle"></i> Informations Générales</h3>
                                        <div style="display: flex; gap: 1rem;">
                                            <button type="submit" name="modifier_villa" class="btn btn-success">
                                                <i class="fas fa-save"></i> Sauvegarder
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
                            <!-- À continuer dans la suite... -->
                        </div>
                        
                        <!-- ONGLET HISTORIQUE -->
                        <div id="tab-historique" class="tab-content <?= $activeTab === 'historique' ? 'active' : '' ?>">
                            <!-- À continuer dans la suite... -->
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
            console.log('Chargement onglet images...');
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
    </style>
</body>
</html>