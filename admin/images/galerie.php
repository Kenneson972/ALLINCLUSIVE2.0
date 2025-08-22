<?php
/**
 * Galerie globale des images - KhanelConcept Admin
 * Vue d'ensemble de toutes les images avec filtrage et gestion avancée
 */

require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../includes/functions.php';

requireAuth();

$villaManager = new VillaManager();
$success = '';
$error = '';

// Traitement des actions en lot
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['bulk_action'])) {
    if (!validateCSRFToken($_POST['csrf_token'])) {
        $error = 'Token de sécurité invalide';
    } else {
        $selected_images = $_POST['selected_images'] ?? [];
        $bulk_action = $_POST['bulk_action'];
        
        if (!empty($selected_images)) {
            try {
                switch ($bulk_action) {
                    case 'delete':
                        $deleted_count = 0;
                        foreach ($selected_images as $image_id) {
                            if ($villaManager->deleteVillaImage($image_id)) {
                                $deleted_count++;
                            }
                        }
                        $success = "$deleted_count image(s) supprimée(s) avec succès";
                        break;
                        
                    case 'reassign':
                        $new_villa_id = $_POST['reassign_villa_id'] ?? null;
                        if ($new_villa_id) {
                            $reassigned_count = 0;
                            foreach ($selected_images as $image_id) {
                                if ($villaManager->reassignImage($image_id, $new_villa_id)) {
                                    $reassigned_count++;
                                }
                            }
                            $success = "$reassigned_count image(s) réassignée(s) avec succès";
                        } else {
                            $error = 'Veuillez sélectionner une villa de destination';
                        }
                        break;
                }
            } catch (Exception $e) {
                $error = 'Erreur lors de l\'opération : ' . $e->getMessage();
            }
        } else {
            $error = 'Aucune image sélectionnée';
        }
    }
}

// Récupération des données
$filter_villa = $_GET['villa'] ?? '';
$all_villas = $villaManager->getAllVillas();

// Récupération des images avec filtrage
if ($filter_villa) {
    $images = $villaManager->getVillaImages($filter_villa);
} else {
    // Récupérer toutes les images avec informations des villas
    $stmt = $villaManager->pdo->query("
        SELECT vi.*, v.nom as villa_nom, v.slug as villa_slug, v.type as villa_type
        FROM villa_images vi
        LEFT JOIN villas v ON vi.villa_id = v.id
        ORDER BY vi.ordre ASC, vi.date_upload DESC
    ");
    $images = $stmt->fetchAll();
}

// Calcul des statistiques
$stats_stmt = $villaManager->pdo->query("
    SELECT 
        COUNT(*) as total_images,
        SUM(taille_fichier) as total_size,
        COUNT(DISTINCT villa_id) as villas_with_images
    FROM villa_images
");
$stats = $stats_stmt->fetch();

$total_size_mb = $stats['total_size'] ? round($stats['total_size'] / (1024 * 1024), 2) : 0;
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galerie Images - KhanelConcept Admin</title>
    <link rel="stylesheet" href="../assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .image-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            overflow: hidden;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .image-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .image-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .image-info {
            padding: 1rem;
        }
        
        .image-title {
            font-weight: 600;
            color: white;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        
        .image-meta {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
            margin: 0.25rem 0;
        }
        
        .image-villa-badge {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            margin: 0.5rem 0;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            color: white;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #ffd700;
            margin-bottom: 0.5rem;
        }
        
        .bulk-actions {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            display: none;
        }
        
        .bulk-actions.show {
            display: block;
        }
        
        .image-selector {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 20px;
            height: 20px;
        }
        
        .filter-bar {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        
        .loading-overlay.show {
            opacity: 1;
            visibility: visible;
        }
        
        .loading-content {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            color: white;
        }
        
        .spinner {
            font-size: 3rem;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }
        
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <!-- Overlay de chargement -->
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-content">
            <div class="spinner"><i class="fas fa-spinner"></i></div>
            <p>Traitement en cours...</p>
        </div>
    </div>

    <div class="admin-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo">
                <h2><i class="fas fa-images"></i> Galerie</h2>
            </div>
            <nav>
                <ul>
                    <li><a href="../index.php"><i class="fas fa-dashboard"></i> Dashboard</a></li>
                    <li><a href="../villas/liste.php"><i class="fas fa-home"></i> Villas</a></li>
                    <li><a href="../villas/ajouter.php"><i class="fas fa-plus"></i> Ajouter Villa</a></li>
                    <li class="active"><a href="galerie.php"><i class="fas fa-images"></i> Galerie</a></li>
                    <li><a href="upload.php"><i class="fas fa-upload"></i> Upload</a></li>
                    <li><a href="../api/villas.php" target="_blank"><i class="fas fa-code"></i> API JSON</a></li>
                </ul>
            </nav>
            <div class="user-info">
                <div class="user-avatar">
                    <i class="fas fa-user-shield"></i>
                </div>
                <div class="user-details">
                    <span class="user-name"><?= htmlspecialchars($_SESSION['admin_name']) ?></span>
                    <span class="user-role">Administrateur</span>
                </div>
                <a href="../logout.php" class="logout-btn">
                    <i class="fas fa-sign-out-alt"></i>
                </a>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="main-content">
            <header class="content-header">
                <div class="header-left">
                    <h1><i class="fas fa-images"></i> Galerie des Images</h1>
                    <p class="subtitle">Gestion globale de toutes les images</p>
                </div>
                <div class="header-actions">
                    <a href="upload.php" class="btn btn-success">
                        <i class="fas fa-plus"></i> Upload Images
                    </a>
                </div>
            </header>

            <?php if ($success): ?>
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i>
                    <?= htmlspecialchars($success) ?>
                </div>
            <?php endif; ?>

            <?php if ($error): ?>
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-triangle"></i>
                    <?= htmlspecialchars($error) ?>
                </div>
            <?php endif; ?>

            <!-- Statistiques globales -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number"><?= $stats['total_images'] ?></div>
                    <div>Images totales</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><?= $total_size_mb ?> MB</div>
                    <div>Espace utilisé</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><?= $stats['villas_with_images'] ?></div>
                    <div>Villas avec images</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number"><?= count($all_villas) ?></div>
                    <div>Total villas</div>
                </div>
            </div>

            <!-- Barre de filtrage -->
            <div class="filter-bar">
                <form method="GET" class="filter-form" style="display: flex; gap: 1rem; align-items: center; flex: 1;">
                    <label for="villa" style="color: white; font-weight: 600;">
                        <i class="fas fa-filter"></i> Filtrer par villa :
                    </label>
                    <select name="villa" id="villa" onchange="this.form.submit()" style="padding: 0.5rem; border-radius: 5px; border: none; background: rgba(255,255,255,0.2); color: white;">
                        <option value="">Toutes les villas</option>
                        <?php foreach ($all_villas as $villa): ?>
                            <option value="<?= $villa['id'] ?>" <?= $filter_villa == $villa['id'] ? 'selected' : '' ?>>
                                <?= htmlspecialchars($villa['nom']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                </form>
                
                <div style="display: flex; gap: 0.5rem;">
                    <button onclick="selectAll()" class="btn btn-sm btn-secondary">
                        <i class="fas fa-check-double"></i> Tout sélectionner
                    </button>
                    <button onclick="clearSelection()" class="btn btn-sm btn-secondary">
                        <i class="fas fa-times"></i> Désélectionner
                    </button>
                </div>
            </div>

            <!-- Actions en lot -->
            <div class="bulk-actions" id="bulkActions">
                <form method="POST" onsubmit="return confirmBulkAction(event)" style="display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    <input type="hidden" name="selected_images_input" id="selectedImagesInput">
                    
                    <span style="color: white; font-weight: 600;">
                        <span id="selectedCount">0</span> image(s) sélectionnée(s)
                    </span>
                    
                    <select name="bulk_action" required style="padding: 0.5rem; border-radius: 5px; border: none; background: rgba(255,255,255,0.2); color: white;">
                        <option value="">Choisir une action...</option>
                        <option value="delete">🗑️ Supprimer</option>
                        <option value="reassign">📤 Réassigner à une villa</option>
                    </select>
                    
                    <select name="reassign_villa_id" style="padding: 0.5rem; border-radius: 5px; border: none; background: rgba(255,255,255,0.2); color: white; display: none;" id="reassignSelect">
                        <option value="">Choisir la villa...</option>
                        <?php foreach ($all_villas as $villa): ?>
                            <option value="<?= $villa['id'] ?>">
                                <?= htmlspecialchars($villa['nom']) ?>
                            </option>
                        <?php endforeach; ?>
                    </select>
                    
                    <button type="submit" class="btn btn-warning">
                        <i class="fas fa-bolt"></i> Exécuter
                    </button>
                </form>
            </div>

            <!-- Grille des images -->
            <div class="gallery-grid">
                <?php if (empty($images)): ?>
                    <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: rgba(255,255,255,0.7);">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">
                            <i class="fas fa-image"></i>
                        </div>
                        <h3>Aucune image trouvée</h3>
                        <p>
                            <?= $filter_villa ? 'Cette villa n\'a pas encore d\'images.' : 'Commencez par uploader des images pour vos villas.' ?>
                        </p>
                        <a href="upload.php" class="btn btn-primary" style="margin-top: 1rem;">
                            <i class="fas fa-plus"></i> Ajouter des images
                        </a>
                    </div>
                <?php else: ?>
                    <?php foreach ($images as $image): ?>
                        <div class="image-card" data-image-id="<?= $image['id'] ?>">
                            <input type="checkbox" class="image-selector" data-image-id="<?= $image['id'] ?>" onchange="updateBulkActions()">
                            
                            <img src="../uploads/villas/<?= htmlspecialchars($image['nom_fichier']) ?>" 
                                 alt="<?= htmlspecialchars($image['alt_text']) ?>"
                                 onerror="this.src='../assets/images/placeholder.jpg'">
                            
                            <div class="image-info">
                                <div class="image-title">
                                    <?= htmlspecialchars($image['alt_text'] ?: $image['nom_fichier']) ?>
                                </div>
                                
                                <?php if ($image['villa_nom']): ?>
                                    <div class="image-villa-badge">
                                        <i class="fas fa-home"></i>
                                        <?= htmlspecialchars($image['villa_nom']) ?>
                                    </div>
                                <?php else: ?>
                                    <div class="image-villa-badge" style="background: #dc3545;">
                                        <i class="fas fa-exclamation"></i>
                                        Non assignée
                                    </div>
                                <?php endif; ?>
                                
                                <div class="image-meta">
                                    <i class="fas fa-calendar"></i>
                                    <?= date('d/m/Y', strtotime($image['date_upload'])) ?>
                                </div>
                                
                                <div class="image-meta">
                                    <i class="fas fa-hdd"></i>
                                    <?= formatFileSize($image['taille_fichier']) ?>
                                </div>
                                
                                <?php if ($image['largeur'] && $image['hauteur']): ?>
                                    <div class="image-meta">
                                        <i class="fas fa-expand"></i>
                                        <?= $image['largeur'] ?> × <?= $image['hauteur'] ?>px
                                    </div>
                                <?php endif; ?>
                                
                                <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                                    <?php if ($image['villa_nom']): ?>
                                        <a href="../villas/modifier.php?id=<?= $image['villa_id'] ?>&tab=images" 
                                           class="btn btn-sm btn-primary">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                    <?php endif; ?>
                                    
                                    <button onclick="deleteImage(<?= $image['id'] ?>)" 
                                            class="btn btn-sm btn-danger">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    <?php endforeach; ?>
                <?php endif; ?>
            </div>
        </main>
    </div>

    <script src="../assets/js/admin.js"></script>
    <script>
        // Gestion des sélections multiples
        function updateBulkActions() {
            const checkboxes = document.querySelectorAll('.image-selector:checked');
            const bulkActions = document.getElementById('bulkActions');
            const selectedCount = document.getElementById('selectedCount');
            const selectedInput = document.getElementById('selectedImagesInput');
            
            selectedCount.textContent = checkboxes.length;
            
            if (checkboxes.length > 0) {
                bulkActions.classList.add('show');
                
                // Mettre à jour la liste des IDs sélectionnés
                const selectedIds = Array.from(checkboxes).map(cb => cb.dataset.imageId);
                selectedInput.value = selectedIds.join(',');
                
                // Convertir en input hidden multiple pour PHP
                const existingInputs = document.querySelectorAll('input[name="selected_images[]"]');
                existingInputs.forEach(input => input.remove());
                
                selectedIds.forEach(id => {
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = 'selected_images[]';
                    hiddenInput.value = id;
                    bulkActions.querySelector('form').appendChild(hiddenInput);
                });
                
            } else {
                bulkActions.classList.remove('show');
            }
        }
        
        // Sélectionner/Désélectionner tout
        function selectAll() {
            document.querySelectorAll('.image-selector').forEach(cb => {
                cb.checked = true;
            });
            updateBulkActions();
        }
        
        function clearSelection() {
            document.querySelectorAll('.image-selector').forEach(cb => {
                cb.checked = false;
            });
            updateBulkActions();
        }
        
        // Afficher/masquer le select de réassignation
        document.querySelector('select[name="bulk_action"]').addEventListener('change', function() {
            const reassignSelect = document.getElementById('reassignSelect');
            if (this.value === 'reassign') {
                reassignSelect.style.display = 'block';
                reassignSelect.required = true;
            } else {
                reassignSelect.style.display = 'none';
                reassignSelect.required = false;
            }
        });
        
        // Confirmation des actions en lot
        function confirmBulkAction(event) {
            const action = event.target.bulk_action.value;
            const count = document.querySelectorAll('.image-selector:checked').length;
            
            let message = '';
            if (action === 'delete') {
                message = `Êtes-vous sûr de vouloir supprimer ${count} image(s) ? Cette action est irréversible.`;
            } else if (action === 'reassign') {
                const villaSelect = event.target.reassign_villa_id;
                const villaName = villaSelect.options[villaSelect.selectedIndex].text;
                message = `Êtes-vous sûr de vouloir réassigner ${count} image(s) à "${villaName}" ?`;
            }
            
            if (message && !confirm(message)) {
                event.preventDefault();
                return false;
            }
            
            // Afficher le loading
            document.getElementById('loadingOverlay').classList.add('show');
            return true;
        }
        
        // Suppression individuelle
        async function deleteImage(imageId) {
            if (!confirm('Êtes-vous sûr de vouloir supprimer cette image ?')) {
                return;
            }
            
            document.getElementById('loadingOverlay').classList.add('show');
            
            try {
                const formData = new FormData();
                formData.append('bulk_action', 'delete');
                formData.append('selected_images[]', imageId);
                formData.append('csrf_token', '<?= generateCSRFToken() ?>');
                
                const response = await fetch('', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    location.reload();
                } else {
                    alert('Erreur lors de la suppression');
                    document.getElementById('loadingOverlay').classList.remove('show');
                }
            } catch (error) {
                alert('Erreur de connexion');
                document.getElementById('loadingOverlay').classList.remove('show');
            }
        }
    </script>
</body>
</html>