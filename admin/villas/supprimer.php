<?php
/**
 * Suppression sécurisée des villas - KhanelConcept Admin
 * Module de suppression avec confirmation et gestion des images
 */

require_once __DIR__ . '/../includes/config.php';
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../includes/functions.php';

requireAuth();

$villaManager = new VillaManager();
$pdo = Database::getInstance()->getConnection();
$error = '';

// Récupération de l'ID villa
$villa_id = $_GET['id'] ?? null;
if (!$villa_id || !is_numeric($villa_id)) {
    redirect('liste.php');
    exit;
}

// Récupération des détails de la villa
$villa = $villaManager->getVillaById($villa_id);
if (!$villa) {
    redirect('liste.php');
    exit;
}

// Récupération des images associées
$images = $villaManager->getVillaImages($villa_id);

// Traitement de la suppression
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!validateCSRFToken($_POST['csrf_token'])) {
        $error = 'Token de sécurité invalide';
    } else {
        $confirm_name = $_POST['confirm_name'] ?? '';
        $image_action = $_POST['image_action'] ?? 'unassign';
        $reassign_villa_id = $_POST['reassign_villa_id'] ?? null;
        
        // Vérification du nom de confirmation
        if (strtolower(trim($confirm_name)) !== strtolower(trim($villa['nom']))) {
            $error = 'Le nom de confirmation ne correspond pas';
        } else {
            try {
                $pdo->beginTransaction();
                
                // Gestion des images selon le choix
                foreach ($images as $image) {
                    if ($image_action === 'reassign' && $reassign_villa_id) {
                        // Réassigner à une autre villa
                        $stmt = $pdo->prepare("UPDATE villa_images SET villa_id = ? WHERE id = ?");
                        $stmt->execute([$reassign_villa_id, $image['id']]);
                    } elseif ($image_action === 'unassign') {
                        // Déplacer vers la galerie "Non assignées"
                        $unassignedId = $villaManager->getOrCreateUnassignedVillaId();
                        $stmt = $pdo->prepare("UPDATE villa_images SET villa_id = ? WHERE id = ?");
                        $stmt->execute([$unassignedId, $image['id']]);
                    } else {
                        // Supprimer les fichiers images
                        $image_path = UPLOAD_PATH . $image['nom_fichier'];
                        if (file_exists($image_path)) {
                            @unlink($image_path);
                        }
                        // Supprimer de la BDD
                        $stmt = $pdo->prepare("DELETE FROM villa_images WHERE id = ?");
                        $stmt->execute([$image['id']]);
                    }
                }
                
                // Supprimer la villa de la BDD
                $stmt = $pdo->prepare("DELETE FROM villas WHERE id = ?");
                $stmt->execute([$villa_id]);
                
                // Supprimer la page HTML générée si elle existe
                $html_file = __DIR__ . '/../../frontend/public/villa-' . $villa['slug'] . '.html';
                if (file_exists($html_file)) {
                    @unlink($html_file);
                }
                
                $pdo->commit();
                
                // Redirection avec message de succès
                $_SESSION['success_message'] = "Villa \"{$villa['nom']}\" supprimée avec succès";
                redirect('liste.php');
                
            } catch (Exception $e) {
                $pdo->rollBack();
                $error = 'Erreur lors de la suppression : ' . $e->getMessage();
            }
        }
    }
}

// Récupération des autres villas pour réassignation
$other_villas = [];
if (!empty($images)) {
    $stmt = $pdo->prepare("SELECT id, nom FROM villas WHERE id != ? ORDER BY nom");
    $stmt->execute([$villa_id]);
    $other_villas = $stmt->fetchAll();
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Supprimer Villa - KhanelConcept Admin</title>
    <link rel="stylesheet" href="../assets/css/admin.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .danger-zone { background: rgba(220, 53, 69, 0.1); border: 2px solid rgba(220, 53, 69, 0.3); border-radius: 15px; padding: 2rem; margin: 2rem 0; backdrop-filter: blur(20px); }
        .danger-title { color: #ff6b6b; font-size: 1.5rem; font-weight: bold; margin-bottom: 1rem; text-align: center; }
        .villa-details { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; padding: 1.5rem; margin: 1.5rem 0; }
        .villa-detail-item { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); color: white; }
        .villa-detail-item:last-child { border-bottom: none; }
        .villa-detail-label { font-weight: 600; color: rgba(255, 255, 255, 0.8); }
        .villa-detail-value { font-weight: 500; }
        .images-preview { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
        .image-preview { position: relative; border-radius: 8px; overflow: hidden; aspect-ratio: 1; }
        .image-preview img { width: 100%; height: 100%; object-fit: cover; }
        .image-action-selector { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; padding: 1.5rem; margin: 1.5rem 0; }
        .radio-group { display: flex; flex-direction: column; gap: 1rem; }
        .radio-option { display: flex; align-items: center; padding: 1rem; background: rgba(255, 255, 255, 0.05); border: 2px solid transparent; border-radius: 10px; cursor: pointer; transition: all 0.3s ease; color: white; }
        .radio-option:hover { background: rgba(255, 255, 255, 0.1); border-color: rgba(255, 255, 255, 0.2); }
        .radio-option.selected { border-color: #667eea; background: rgba(102, 126, 234, 0.2); }
        .radio-option input[type="radio"] { margin-right: 1rem; transform: scale(1.2); }
        .radio-option-icon { font-size: 1.5rem; margin-right: 1rem; min-width: 2rem; }
        .radio-option-content h4 { margin: 0 0 0.5rem 0; color: white; }
        .radio-option-content p { margin: 0; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; }
        .confirmation-input { margin: 1.5rem 0; }
        .confirmation-input label { display: block; color: white; font-weight: 600; margin-bottom: 0.5rem; }
        .confirmation-input input { width: 100%; padding: 0.75rem; border: 2px solid rgba(220, 53, 69, 0.5); border-radius: 8px; background: rgba(255, 255, 255, 0.1); color: white; font-size: 1rem; }
        .confirmation-input input:focus { border-color: #ff6b6b; outline: none; box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.2); }
        .warning-message { background: rgba(255, 193, 7, 0.2); border: 1px solid rgba(255, 193, 7, 0.5); border-radius: 8px; padding: 1rem; margin: 1rem 0; color: #ffc107; text-align: center; font-weight: 600; }
        .btn-danger-confirm { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; font-size: 1rem; }
        .btn-danger-confirm:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4); }
        .btn-danger-confirm:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }
        .back-link { display: inline-flex; align-items: center; color: rgba(255, 255, 255, 0.8); text-decoration: none; margin-bottom: 2rem; padding: 0.5rem 1rem; border-radius: 8px; background: rgba(255, 255, 255, 0.1); transition: all 0.3s ease; }
        .back-link:hover { color: white; background: rgba(255, 255, 255, 0.2); transform: translateX(-5px); }
        .back-link i { margin-right: 0.5rem; }
    </style>
</head>
<body>
    <div class="admin-container">
        <!-- Sidebar -->
        <aside class="sidebar">
            <div class="logo">
                <h2><i class="fas fa-trash-alt"></i> Supprimer</h2>
            </div>
            <nav>
                <ul>
                    <li><a href="../index.php"><i class="fas fa-dashboard"></i> Dashboard</a></li>
                    <li><a href="liste.php"><i class="fas fa-home"></i> Villas</a></li>
                    <li><a href="ajouter.php"><i class="fas fa-plus"></i> Ajouter Villa</a></li>
                    <li><a href="../images/galerie.php"><i class="fas fa-images"></i> Galerie</a></li>
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
            <a href="liste.php" class="back-link">
                <i class="fas fa-arrow-left"></i>
                Retour à la liste des villas
            </a>

            <header class="content-header">
                <div class="header-left">
                    <h1><i class="fas fa-trash-alt"></i> Supprimer Villa</h1>
                    <p class="subtitle">Suppression définitive avec gestion des fichiers</p>
                </div>
            </header>

            <?php if ($error): ?>
                <div class="alert alert-error">
                    <i class="fas fa-exclamation-triangle"></i>
                    <?= htmlspecialchars($error) ?>
                </div>
            <?php endif; ?>

            <!-- Zone de danger -->
            <div class="danger-zone">
                <div class="danger-title">
                    <i class="fas fa-exclamation-triangle"></i>
                    ZONE DE DANGER
                </div>
                
                <div class="warning-message">
                    <i class="fas fa-exclamation-circle"></i>
                    Vous êtes sur le point de supprimer définitivement cette villa. Cette action est IRRÉVERSIBLE.
                </div>

                <!-- Détails de la villa -->
                <div class="villa-details">
                    <h3 style="color: white; margin-bottom: 1rem;">
                        <i class="fas fa-info-circle"></i>
                        Détails de la villa à supprimer
                    </h3>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Nom :</span>
                        <span class="villa-detail-value"><?= htmlspecialchars($villa['nom']) ?></span>
                    </div>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Type :</span>
                        <span class="villa-detail-value"><?= htmlspecialchars($villa['type']) ?></span>
                    </div>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Localisation :</span>
                        <span class="villa-detail-value"><?= htmlspecialchars($villa['localisation']) ?></span>
                    </div>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Prix par nuit :</span>
                        <span class="villa-detail-value"><?= formatPrice($villa['prix_nuit']) ?></span>
                    </div>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Capacité :</span>
                        <span class="villa-detail-value"><?= (int)$villa['capacite_max'] ?> personnes</span>
                    </div>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Créée le :</span>
                        <span class="villa-detail-value"><?= !empty($villa['created_at']) ? date('d/m/Y à H:i', strtotime($villa['created_at'])) : '-' ?></span>
                    </div>
                    
                    <div class="villa-detail-item">
                        <span class="villa-detail-label">Images associées :</span>
                        <span class="villa-detail-value"><?= count($images) ?> fichier(s)</span>
                    </div>
                </div>

                <!-- Aperçu des images -->
                <?php if (!empty($images)): ?>
                    <div style="margin: 1.5rem 0;">
                        <h4 style="color: white; margin-bottom: 1rem;">
                            <i class="fas fa-images"></i>
                            Images qui seront affectées (<?= count($images) ?>)
                        </h4>
                        
                        <div class="images-preview">
                            <?php foreach (array_slice($images, 0, 6) as $image): ?>
                                <div class="image-preview">
                                    <img src="../uploads/villas/<?= htmlspecialchars($image['nom_fichier']) ?>" 
                                         alt="<?= htmlspecialchars($image['alt_text']) ?>">
                                </div>
                            <?php endforeach; ?>
                            
                            <?php if (count($images) > 6): ?>
                                <div class="image-preview" style="display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.1); color: white;">
                                    <div style="text-align: center;">
                                        <div style="font-size: 2rem;">+<?= count($images) - 6 ?></div>
                                        <div style="font-size: 0.8rem;">images</div>
                                    </div>
                                </div>
                            <?php endif; ?>
                        </div>
                    </div>
                <?php endif; ?>

                <!-- Formulaire de suppression -->
                <form method="POST" onsubmit="return confirmDeletion(event)" style="margin-top: 2rem;">
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    
                    <!-- Gestion des images -->
                    <?php if (!empty($images)): ?>
                        <div class="image-action-selector">
                            <h4 style="color: white; margin-bottom: 1rem;">
                                <i class="fas fa-cog"></i>
                                Que faire avec les <?= count($images) ?> image(s) ?
                            </h4>
                            
                            <div class="radio-group">
                                <label class="radio-option selected" onclick="selectOption(this, 'unassign')">
                                    <input type="radio" name="image_action" value="unassign" checked>
                                    <div class="radio-option-icon">📦</div>
                                    <div class="radio-option-content">
                                        <h4>Déplacer vers la galerie "Non assignées"</h4>
                                        <p>Conserve les fichiers et les déplace dans une galerie sécurisée (recommandé)</p>
                                    </div>
                                </label>
                                
                                <?php if (!empty($other_villas)): ?>
                                    <label class="radio-option" onclick="selectOption(this, 'reassign')">
                                        <input type="radio" name="image_action" value="reassign">
                                        <div class="radio-option-icon">📤</div>
                                        <div class="radio-option-content">
                                            <h4>Réassigner à une autre villa</h4>
                                            <p>Transférer les images vers une villa existante</p>
                                        </div>
                                    </label>
                                    
                                    <div id="reassignSelect" style="display: none; margin-top: 1rem;">
                                        <label for="reassign_villa_id" style="color: white; display: block; margin-bottom: 0.5rem;">
                                            Villa de destination :
                                        </label>
                                        <select name="reassign_villa_id" id="reassign_villa_id" style="width: 100%; padding: 0.75rem; border-radius: 8px; border: none; background: rgba(255,255,255,0.2); color: white;">
                                            <option value="">Choisir une villa...</option>
                                            <?php foreach ($other_villas as $other_villa): ?>
                                                <option value="<?= (int)$other_villa['id'] ?>">
                                                    <?= htmlspecialchars($other_villa['nom']) ?>
                                                </option>
                                            <?php endforeach; ?>
                                        </select>
                                    </div>
                                <?php endif; ?>
                                
                                <label class="radio-option" onclick="selectOption(this, 'delete')">
                                    <input type="radio" name="image_action" value="delete">
                                    <div class="radio-option-icon">🗑️</div>
                                    <div class="radio-option-content">
                                        <h4>Supprimer définitivement</h4>
                                        <p>Toutes les images seront supprimées du serveur</p>
                                    </div>
                                </label>
                            </div>
                        </div>
                    <?php else: ?>
                        <input type="hidden" name="image_action" value="delete">
                    <?php endif; ?>
                    
                    <!-- Confirmation par nom -->
                    <div class="confirmation-input">
                        <label for="confirm_name">
                            <i class="fas fa-shield-alt"></i>
                            Pour confirmer, tapez le nom exact de la villa :
                        </label>
                        <input type="text" id="confirm_name" name="confirm_name" required autocomplete="off" placeholder="<?= htmlspecialchars($villa['nom']) ?>" onkeyup="validateConfirmation()">
                        <small style="color: rgba(255,255,255,0.6); display: block; margin-top: 0.5rem;">
                            Nom à saisir : <strong><?= htmlspecialchars($villa['nom']) ?></strong>
                        </small>
                    </div>
                    
                    <!-- Boutons d'action -->
                    <div style="text-align: center; margin-top: 2rem;">
                        <a href="liste.php" class="btn btn-secondary" style="margin-right: 1rem;">
                            <i class="fas fa-times"></i>
                            Annuler
                        </a>
                        
                        <button type="submit" class="btn-danger-confirm" id="deleteButton" disabled>
                            <i class="fas fa-trash-alt"></i>
                            SUPPRIMER DÉFINITIVEMENT
                        </button>
                    </div>
                </form>
            </div>
        </main>
    </div>

    <script>
        // Validation de la confirmation
        function validateConfirmation() {
            const input = document.getElementById('confirm_name');
            const button = document.getElementById('deleteButton');
            const expectedName = "<?= addslashes($villa['nom']) ?>";
            if (input.value.trim().toLowerCase() === expectedName.toLowerCase()) {
                button.disabled = false;
                input.style.borderColor = '#28a745';
            } else {
                button.disabled = true;
                input.style.borderColor = 'rgba(220, 53, 69, 0.5)';
            }
        }
        
        // Sélection des options radio
        function selectOption(element, action) {
            document.querySelectorAll('.radio-option').forEach(opt => { opt.classList.remove('selected'); });
            element.classList.add('selected');
            const reassignSelect = document.getElementById('reassignSelect');
            if (action === 'reassign' && reassignSelect) {
                reassignSelect.style.display = 'block';
                document.getElementById('reassign_villa_id').required = true;
            } else if (reassignSelect) {
                reassignSelect.style.display = 'none';
                document.getElementById('reassign_villa_id').required = false;
            }
        }
        
        // Confirmation finale
        function confirmDeletion(event) {
            const villa_name = "<?= addslashes($villa['nom']) ?>";
            const image_count = <?= count($images) ?>;
            const action = document.querySelector('input[name="image_action"]:checked').value;
            
            let message = `ATTENTION : Vous allez supprimer définitivement la villa "${villa_name}".`;
            if (image_count > 0) {
                if (action === 'delete') {
                    message += `\n\n${image_count} image(s) seront également supprimée(s) du serveur.`;
                } else if (action === 'reassign') {
                    const targetVilla = document.getElementById('reassign_villa_id');
                    if (!targetVilla.value) {
                        alert('Veuillez sélectionner une villa de destination pour les images.');
                        event.preventDefault();
                        return false;
                    }
                    const targetName = targetVilla.options[targetVilla.selectedIndex].text;
                    message += `\n\n${image_count} image(s) seront transférée(s) vers "${targetName}".`;
                } else if (action === 'unassign') {
                    message += `\n\n${image_count} image(s) seront déplacée(s) vers la galerie \"Non assignées\".`;
                }
            }
            message += '\n\nCette action est IRRÉVERSIBLE. Êtes-vous absolument certain(e) ?';
            if (!confirm(message)) {
                event.preventDefault();
                return false;
            }
            return true;
        }
    </script>
</body>
</html>