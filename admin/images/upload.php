<?php
/**
 * Upload d'images - KhanelConcept Admin
 */

require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

// Vérifier l'authentification
requireAuth();

$villaManager = new VillaManager();
$currentUser = getCurrentUser();

// Villa préselectionnée depuis l'URL
$selectedVillaId = isset($_GET['villa_id']) ? (int)$_GET['villa_id'] : null;

// Récupérer toutes les villas pour le sélecteur
$allVillas = $villaManager->getAllVillas();

// Traitement de l'upload AJAX
if ($_POST && isset($_POST['action']) && $_POST['action'] === 'upload') {
    header('Content-Type: application/json');
    
    $villaId = (int)$_POST['villa_id'];
    $altText = trim($_POST['alt_text'] ?? '');
    $imagePrincipale = isset($_POST['image_principale']);
    
    if (!$villaId || !$villaManager->getVillaById($villaId)) {
        echo json_encode(['success' => false, 'error' => 'Villa invalide']);
        exit;
    }
    
    if (!isset($_FILES['image']) || $_FILES['image']['error'] !== UPLOAD_ERR_OK) {
        echo json_encode(['success' => false, 'error' => 'Erreur lors de l\'upload']);
        exit;
    }
    
    // Upload de l'image
    $result = ImageUploader::upload($_FILES['image'], 'villa_' . $villaId . '_');
    
    if ($result['success']) {
        // Enregistrer en base
        $imageId = $villaManager->addVillaImage(
            $villaId, 
            $result['fileName'], 
            $result['originalName'], 
            $altText, 
            $imagePrincipale
        );
        
        if ($imageId) {
            echo json_encode([
                'success' => true,
                'message' => 'Image uploadée avec succès',
                'data' => [
                    'id' => $imageId,
                    'filename' => $result['fileName'],
                    'url' => UPLOAD_URL . $result['fileName'],
                    'size' => $result['size'],
                    'dimensions' => $result['dimensions']
                ]
            ]);
        } else {
            // Supprimer le fichier si erreur BDD
            unlink(UPLOAD_PATH . $result['fileName']);
            echo json_encode(['success' => false, 'error' => 'Erreur lors de l\'enregistrement']);
        }
    } else {
        echo json_encode(['success' => false, 'error' => $result['error']]);
    }
    exit;
}

// Traitement suppression d'image
if ($_POST && isset($_POST['action']) && $_POST['action'] === 'delete_image') {
    header('Content-Type: application/json');
    
    $imageId = (int)$_POST['image_id'];
    
    if ($villaManager->deleteImage($imageId)) {
        echo json_encode(['success' => true, 'message' => 'Image supprimée']);
    } else {
        echo json_encode(['success' => false, 'error' => 'Erreur lors de la suppression']);
    }
    exit;
}

// Traitement définir image principale
if ($_POST && isset($_POST['action']) && $_POST['action'] === 'set_main_image') {
    header('Content-Type: application/json');
    
    $imageId = (int)$_POST['image_id'];
    $villaId = (int)$_POST['villa_id'];
    
    if ($villaManager->setMainImage($villaId, $imageId)) {
        echo json_encode(['success' => true, 'message' => 'Image principale définie']);
    } else {
        echo json_encode(['success' => false, 'error' => 'Erreur lors de la mise à jour']);
    }
    exit;
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload d'Images - KhanelConcept Admin</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="../assets/css/admin.css">
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
                <li><a href="../villas/liste.php"><i class="fas fa-home"></i> Villas</a></li>
                <li><a href="../villas/ajouter.php"><i class="fas fa-plus"></i> Ajouter Villa</a></li>
                <li><a href="galerie.php"><i class="fas fa-images"></i> Galerie</a></li>
                <li><a href="upload.php" class="active"><i class="fas fa-upload"></i> Upload Images</a></li>
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
                    <h2><i class="fas fa-upload"></i> Upload d'Images</h2>
                    <p>Ajouter des photos à vos villas</p>
                </div>
                <div class="header-actions">
                    <a href="galerie.php" class="btn btn-primary">
                        <i class="fas fa-images"></i> Voir la galerie
                    </a>
                </div>
            </header>
            
            <!-- Zone de contenu -->
            <div class="content-area">
                <?php displayFlashMessage(); ?>
                
                <!-- Sélection de villa -->
                <div class="glass-card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-home"></i> Sélectionner une Villa</h3>
                    </div>
                    
                    <div class="form-group">
                        <select id="villa-select" class="form-control" style="max-width: 400px;">
                            <option value="">Choisir une villa...</option>
                            <?php foreach ($allVillas as $villa): ?>
                                <option value="<?= $villa['id'] ?>" 
                                        <?= $selectedVillaId == $villa['id'] ? 'selected' : '' ?>>
                                    <?= sanitizeHtml($villa['nom']) ?> - <?= sanitizeHtml($villa['type']) ?>
                                </option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                </div>
                
                <!-- Zone d'upload -->
                <div id="upload-section" class="glass-card" style="<?= !$selectedVillaId ? 'display: none;' : '' ?>">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-cloud-upload-alt"></i> Upload d'Images</h3>
                        <div id="selected-villa-info" style="font-size: 0.9rem; color: rgba(255,255,255,0.8);"></div>
                    </div>
                    
                    <!-- Zone de drop -->
                    <div id="drop-zone" class="upload-zone">
                        <div class="upload-icon">
                            <i class="fas fa-cloud-upload-alt"></i>
                        </div>
                        <h3 style="color: white; margin-bottom: 0.5rem;">Glissez vos images ici</h3>
                        <p style="color: rgba(255,255,255,0.8); margin-bottom: 1rem;">
                            ou cliquez pour sélectionner des fichiers
                        </p>
                        <button type="button" class="btn btn-primary" onclick="document.getElementById('file-input').click()">
                            <i class="fas fa-folder-open"></i> Parcourir les fichiers
                        </button>
                        <input type="file" id="file-input" multiple accept="image/*" style="display: none;">
                        
                        <div style="margin-top: 1rem; font-size: 0.8rem; color: rgba(255,255,255,0.6);">
                            <p>Formats acceptés: JPG, PNG, WebP • Taille max: 5MB par image</p>
                            <p>Résolution recommandée: 1920x1080px • Upload multiple supporté</p>
                        </div>
                    </div>
                    
                    <!-- Progress global -->
                    <div id="global-progress" style="display: none; margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="color: white; font-weight: 600;">Upload en cours...</span>
                            <span id="progress-text" style="color: rgba(255,255,255,0.8);">0%</span>
                        </div>
                        <div class="progress-bar">
                            <div id="progress-fill" class="progress-fill"></div>
                        </div>
                    </div>
                    
                    <!-- Queue d'upload -->
                    <div id="upload-queue" style="margin-top: 2rem;"></div>
                </div>
                
                <!-- Images existantes -->
                <div id="existing-images" class="glass-card" style="<?= !$selectedVillaId ? 'display: none;' : '' ?>">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-images"></i> Images Existantes</h3>
                        <span id="images-count" class="badge badge-success">0 image(s)</span>
                    </div>
                    
                    <div id="images-gallery" class="image-gallery">
                        <!-- Images seront chargées ici via JavaScript -->
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script src="../assets/js/admin.js"></script>
    <script>
        let currentVillaId = <?= $selectedVillaId ?? 'null' ?>;
        let uploadQueue = [];
        let activeUploads = 0;
        const maxConcurrentUploads = 3;
        
        document.addEventListener('DOMContentLoaded', function() {
            if (currentVillaId) {
                loadExistingImages(currentVillaId);
                updateVillaInfo(currentVillaId);
            }
            
            setupUploadEvents();
        });
        
        // Gestion du sélecteur de villa
        document.getElementById('villa-select').addEventListener('change', function() {
            currentVillaId = parseInt(this.value) || null;
            
            if (currentVillaId) {
                document.getElementById('upload-section').style.display = 'block';
                document.getElementById('existing-images').style.display = 'block';
                loadExistingImages(currentVillaId);
                updateVillaInfo(currentVillaId);
            } else {
                document.getElementById('upload-section').style.display = 'none';
                document.getElementById('existing-images').style.display = 'none';
            }
        });
        
        function updateVillaInfo(villaId) {
            const select = document.getElementById('villa-select');
            const option = select.querySelector(`option[value="${villaId}"]`);
            if (option) {
                document.getElementById('selected-villa-info').textContent = 
                    `Villa sélectionnée: ${option.textContent}`;
            }
        }
        
        function setupUploadEvents() {
            const dropZone = document.getElementById('drop-zone');
            const fileInput = document.getElementById('file-input');
            
            // Drag & Drop
            dropZone.addEventListener('dragover', handleDragOver);
            dropZone.addEventListener('dragleave', handleDragLeave);
            dropZone.addEventListener('drop', handleDrop);
            
            // Sélection de fichiers
            fileInput.addEventListener('change', function() {
                if (this.files.length > 0) {
                    handleFiles(Array.from(this.files));
                }
            });
            
            // Clic sur la zone
            dropZone.addEventListener('click', function() {
                if (!currentVillaId) {
                    AdminPanel.showToast('Veuillez d\'abord sélectionner une villa', 'error');
                    return;
                }
                fileInput.click();
            });
        }
        
        function handleDragOver(e) {
            e.preventDefault();
            if (!currentVillaId) return;
            this.classList.add('dragover');
        }
        
        function handleDragLeave(e) {
            e.preventDefault();
            this.classList.remove('dragover');
        }
        
        function handleDrop(e) {
            e.preventDefault();
            this.classList.remove('dragover');
            
            if (!currentVillaId) {
                AdminPanel.showToast('Veuillez d\'abord sélectionner une villa', 'error');
                return;
            }
            
            const files = Array.from(e.dataTransfer.files);
            handleFiles(files);
        }
        
        function handleFiles(files) {
            if (!currentVillaId) return;
            
            // Filtrer les images
            const imageFiles = files.filter(file => file.type.startsWith('image/'));
            
            if (imageFiles.length === 0) {
                AdminPanel.showToast('Aucun fichier image valide sélectionné', 'error');
                return;
            }
            
            if (imageFiles.length !== files.length) {
                AdminPanel.showToast(`${files.length - imageFiles.length} fichier(s) ignoré(s) (non-image)`, 'warning');
            }
            
            // Ajouter à la queue
            imageFiles.forEach(file => {
                if (file.size > 5 * 1024 * 1024) {
                    AdminPanel.showToast(`Fichier trop volumineux: ${file.name} (max 5MB)`, 'error');
                    return;
                }
                
                const uploadItem = {
                    id: Date.now() + Math.random(),
                    file: file,
                    villaId: currentVillaId,
                    status: 'pending',
                    progress: 0
                };
                
                uploadQueue.push(uploadItem);
                addToUploadQueue(uploadItem);
            });
            
            processUploadQueue();
        }
        
        function addToUploadQueue(item) {
            const queue = document.getElementById('upload-queue');
            
            const itemElement = document.createElement('div');
            itemElement.id = `upload-item-${item.id}`;
            itemElement.className = 'upload-item';
            itemElement.innerHTML = `
                <div class="upload-item-info">
                    <div class="upload-item-image">
                        <canvas width="60" height="40"></canvas>
                    </div>
                    <div class="upload-item-details">
                        <div class="upload-item-name">${item.file.name}</div>
                        <div class="upload-item-size">${formatFileSize(item.file.size)}</div>
                    </div>
                </div>
                <div class="upload-item-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <div class="upload-item-status">En attente...</div>
                </div>
                <div class="upload-item-actions">
                    <button onclick="removeFromQueue(${item.id})" class="btn-small btn-danger">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            
            queue.appendChild(itemElement);
            
            // Générer preview
            generatePreview(item.file, itemElement.querySelector('canvas'));
        }
        
        function generatePreview(file, canvas) {
            const ctx = canvas.getContext('2d');
            const img = new Image();
            
            img.onload = function() {
                const ratio = Math.min(60/this.width, 40/this.height);
                const width = this.width * ratio;
                const height = this.height * ratio;
                
                canvas.width = 60;
                canvas.height = 40;
                
                ctx.clearRect(0, 0, 60, 40);
                ctx.drawImage(this, (60-width)/2, (40-height)/2, width, height);
            };
            
            img.src = URL.createObjectURL(file);
        }
        
        function processUploadQueue() {
            if (activeUploads >= maxConcurrentUploads) return;
            
            const pendingItem = uploadQueue.find(item => item.status === 'pending');
            if (!pendingItem) return;
            
            uploadFile(pendingItem);
            setTimeout(() => processUploadQueue(), 100);
        }
        
        function uploadFile(item) {
            activeUploads++;
            item.status = 'uploading';
            
            const itemElement = document.getElementById(`upload-item-${item.id}`);
            const progressFill = itemElement.querySelector('.progress-fill');
            const statusElement = itemElement.querySelector('.upload-item-status');
            
            statusElement.textContent = 'Upload en cours...';
            itemElement.classList.add('uploading');
            
            const formData = new FormData();
            formData.append('action', 'upload');
            formData.append('villa_id', item.villaId);
            formData.append('image', item.file);
            formData.append('alt_text', '');
            
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    const progress = (e.loaded / e.total) * 100;
                    progressFill.style.width = progress + '%';
                    item.progress = progress;
                    updateGlobalProgress();
                }
            });
            
            xhr.addEventListener('load', function() {
                activeUploads--;
                
                try {
                    const response = JSON.parse(this.responseText);
                    
                    if (response.success) {
                        item.status = 'completed';
                        statusElement.textContent = 'Terminé';
                        itemElement.classList.add('completed');
                        
                        AdminPanel.showToast(`Image uploadée: ${item.file.name}`, 'success');
                        
                        // Recharger les images existantes
                        setTimeout(() => loadExistingImages(currentVillaId), 1000);
                        
                        // Retirer de la queue après 3s
                        setTimeout(() => {
                            itemElement.remove();
                            uploadQueue = uploadQueue.filter(i => i.id !== item.id);
                        }, 3000);
                        
                    } else {
                        item.status = 'error';
                        statusElement.textContent = 'Erreur: ' + response.error;
                        itemElement.classList.add('error');
                    }
                    
                } catch (e) {
                    item.status = 'error';
                    statusElement.textContent = 'Erreur serveur';
                    itemElement.classList.add('error');
                }
                
                processUploadQueue();
            });
            
            xhr.addEventListener('error', function() {
                activeUploads--;
                item.status = 'error';
                statusElement.textContent = 'Erreur de connexion';
                itemElement.classList.add('error');
                processUploadQueue();
            });
            
            xhr.open('POST', 'upload.php');
            xhr.send(formData);
        }
        
        function updateGlobalProgress() {
            const totalItems = uploadQueue.length;
            const completedItems = uploadQueue.filter(item => item.status === 'completed').length;
            const uploadingItems = uploadQueue.filter(item => item.status === 'uploading');
            
            if (totalItems === 0) {
                document.getElementById('global-progress').style.display = 'none';
                return;
            }
            
            if (uploadingItems.length > 0 || completedItems < totalItems) {
                document.getElementById('global-progress').style.display = 'block';
            }
            
            let totalProgress = completedItems * 100;
            uploadingItems.forEach(item => {
                totalProgress += item.progress;
            });
            
            const overallProgress = Math.round(totalProgress / totalItems);
            document.getElementById('progress-fill').style.width = overallProgress + '%';
            document.getElementById('progress-text').textContent = `${overallProgress}% (${completedItems}/${totalItems})`;
            
            if (completedItems === totalItems) {
                setTimeout(() => {
                    document.getElementById('global-progress').style.display = 'none';
                }, 2000);
            }
        }
        
        function removeFromQueue(itemId) {
            const item = uploadQueue.find(i => i.id === itemId);
            if (item && item.status === 'pending') {
                document.getElementById(`upload-item-${itemId}`).remove();
                uploadQueue = uploadQueue.filter(i => i.id !== itemId);
                updateGlobalProgress();
            }
        }
        
        function loadExistingImages(villaId) {
            // Pour la démo, on simule le chargement
            // Dans la vraie version, il faudrait une API pour récupérer les images
            const gallery = document.getElementById('images-gallery');
            gallery.innerHTML = '<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.6);">Chargement des images...</div>';
            
            // Simulation
            setTimeout(() => {
                gallery.innerHTML = '<div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.6);">Aucune image pour cette villa. Uploadez des images ci-dessus.</div>';
                document.getElementById('images-count').textContent = '0 image(s)';
            }, 1000);
        }
        
        function formatFileSize(bytes) {
            if (bytes === 0) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        }
    </script>
    
    <style>
        .upload-zone {
            min-height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            overflow: hidden;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        .upload-item {
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .upload-item.uploading {
            border-color: rgba(32, 201, 151, 0.5);
        }
        
        .upload-item.completed {
            border-color: rgba(40, 167, 69, 0.5);
        }
        
        .upload-item.error {
            border-color: rgba(220, 53, 69, 0.5);
        }
        
        .upload-item-info {
            display: flex;
            align-items: center;
            gap: 1rem;
            flex: 1;
        }
        
        .upload-item-image canvas {
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .upload-item-name {
            color: white;
            font-weight: 600;
            margin-bottom: 0.25rem;
        }
        
        .upload-item-size {
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.8rem;
        }
        
        .upload-item-progress {
            flex: 1;
            max-width: 200px;
        }
        
        .upload-item-status {
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.8rem;
            margin-top: 0.25rem;
        }
        
        .btn-small {
            padding: 0.25rem 0.5rem;
            font-size: 0.8rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .btn-danger {
            background: rgba(220, 53, 69, 0.8);
            color: white;
        }
        
        .btn-danger:hover {
            background: rgba(220, 53, 69, 1);
        }
        
        .image-gallery {
            min-height: 100px;
        }
    </style>
</body>
</html>