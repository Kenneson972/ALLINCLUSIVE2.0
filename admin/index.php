<?php
/**
 * Dashboard Admin - KhanelConcept
 */

require_once 'includes/config.php';
require_once 'includes/auth.php';
require_once 'includes/functions.php';

// Vérifier l'authentification
requireAuth();

$villaManager = new VillaManager();
$stats = $villaManager->getDashboardStats();
$currentUser = getCurrentUser();
$recentVillas = $villaManager->getAllVillas();
$recentVillas = array_slice($recentVillas, 0, 5); // Limiter à 5
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - KhanelConcept Admin</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="assets/css/admin.css">
    <style>
        .generation-progress { display:none; margin-top: 1rem; }
        .progress-bar { width: 100%; background: rgba(255,255,255,0.15); border-radius: 8px; overflow: hidden; height: 12px; }
        .progress-fill { width: 0%; height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.4s ease; }
        .progress-text { margin-top: 0.5rem; color: rgba(255,255,255,0.9); font-size: 0.9rem; }
        .generation-results { display:none; margin-top: 1rem; padding: 1rem; border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; background: rgba(255,255,255,0.08); }
        .generation-results ul { margin: 0.5rem 0 0 1.25rem; }
    </style>
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
                <li><a href="index.php" class="active"><i class="fas fa-tachometer-alt"></i> Dashboard</a></li>
                <li><a href="villas/liste.php"><i class="fas fa-home"></i> Villas</a></li>
                <li><a href="villas/ajouter.php"><i class="fas fa-plus"></i> Ajouter Villa</a></li>
                <li><a href="images/galerie.php"><i class="fas fa-images"></i> Galerie</a></li>
                <li><a href="api/villas.php" target="_blank"><i class="fas fa-code"></i> API JSON</a></li>
                <li><a href="../" target="_blank"><i class="fas fa-external-link-alt"></i> Voir Site</a></li>
                <li><a href="logout.php"><i class="fas fa-sign-out-alt"></i> Déconnexion</a></li>
            </ul>
        </nav>
        
        <!-- Contenu principal -->
        <main class="main-content">
            <!-- Header -->
            <header class="admin-header">
                <div class="header-title">
                    <h2><i class="fas fa-tachometer-alt"></i> Dashboard</h2>
                    <p>Vue d'ensemble de votre plateforme</p>
                </div>
                <div class="header-actions">
                    <div class="user-info">
                        <div class="user-avatar">
                            <?= strtoupper(substr($currentUser['prenom'] ?? $currentUser['nom'], 0, 1)) ?>
                        </div>
                        <div>
                            <div style="font-weight: 600;"><?= sanitizeHtml($currentUser['prenom'] . ' ' . $currentUser['nom']) ?></div>
                            <div style="font-size: 0.8rem; opacity: 0.8;"><?= sanitizeHtml($currentUser['role']) ?></div>
                        </div>
                    </div>
                </div>
            </header>
            
            <!-- Zone de contenu -->
            <div class="content-area">
                <?php displayFlashMessage(); ?>
                
                <!-- Statistiques -->
                <div class="stats-grid">
                    <div class="stat-card fade-in-up">
                        <div class="stat-icon"><i class="fas fa-home"></i></div>
                        <div class="stat-number"><?= $stats['total_villas'] ?></div>
                        <div class="stat-label">Total Villas</div>
                    </div>
                    
                    <div class="stat-card fade-in-up" style="animation-delay: 0.1s;">
                        <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
                        <div class="stat-number"><?= $stats['villas_disponibles'] ?></div>
                        <div class="stat-label">Disponibles</div>
                    </div>
                    
                    <div class="stat-card fade-in-up" style="animation-delay: 0.2s;">
                        <div class="stat-icon"><i class="fas fa-times-circle"></i></div>
                        <div class="stat-number"><?= $stats['villas_indisponibles'] ?></div>
                        <div class="stat-label">Indisponibles</div>
                    </div>
                    
                    <div class="stat-card fade-in-up" style="animation-delay: 0.3s;">
                        <div class="stat-icon"><i class="fas fa-images"></i></div>
                        <div class="stat-number"><?= $stats['total_images'] ?></div>
                        <div class="stat-label">Total Images</div>
                    </div>
                    
                    <div class="stat-card fade-in-up" style="animation-delay: 0.4s;">
                        <div class="stat-icon"><i class="fas fa-star"></i></div>
                        <div class="stat-number"><?= $stats['villas_featured'] ?></div>
                        <div class="stat-label">En Vedette</div>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem;">
                    <!-- Villas récentes -->
                    <div class="glass-card fade-in-up">
                        <div class="card-header">
                            <h3 class="card-title"><i class="fas fa-clock"></i> Villas Récentes</h3>
                            <a href="villas/liste.php" class="btn btn-primary btn-sm">
                                <i class="fas fa-list"></i> Voir tout
                            </a>
                        </div>
                        
                        <?php if (empty($recentVillas)): ?>
                            <div style="text-align: center; padding: 2rem; color: rgba(255,255,255,0.7);">
                                <i class="fas fa-home" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                                <p>Aucune villa enregistrée pour le moment.</p>
                                <a href="villas/ajouter.php" class="btn btn-success">
                                    <i class="fas fa-plus"></i> Ajouter une villa
                                </a>
                            </div>
                        <?php else: ?>
                            <div class="table-responsive">
                                <table class="table">
                                    <thead>
                                        <tr>
                                            <th>Image</th>
                                            <th>Nom</th>
                                            <th>Type</th>
                                            <th>Prix/Nuit</th>
                                            <th>Statut</th>
                                            <th>Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <?php foreach ($recentVillas as $villa): ?>
                                            <tr>
                                                <td>
                                                    <?php if ($villa['image_principale']): ?>
                                                        <img src="<?= UPLOAD_URL . $villa['image_principale'] ?>" 
                                                             alt="<?= sanitizeHtml($villa['nom']) ?>" 
                                                             class="table-image">
                                                    <?php else: ?>
                                                        <div class="table-image" style="background: rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center;">
                                                            <i class="fas fa-image" style="color: rgba(255,255,255,0.5);"></i>
                                                        </div>
                                                    <?php endif; ?>
                                                </td>
                                                <td>
                                                    <div style="font-weight: 600;"><?= sanitizeHtml($villa['nom']) ?></div>
                                                    <div style="font-size: 0.8rem; opacity: 0.8;">&lt;?= sanitizeHtml($villa['localisation']) ?&gt;</div>
                                                </td>
                                                <td><?= sanitizeHtml($villa['type']) ?></td>
                                                <td style="font-weight: 600; color: #ffc107;"><?= formatPrice($villa['prix_nuit']) ?></td>
                                                <td>
                                                    <?php
                                                    $badgeClass = match($villa['statut']) {
                                                        'disponible' => 'badge-success',
                                                        'indisponible' => 'badge-danger',
                                                        'maintenance' => 'badge-warning',
                                                        default => 'badge-success'
                                                    };
                                                    ?>
                                                    <span class="badge <?= $badgeClass ?>">
                                                        <?= ucfirst($villa['statut']) ?>
                                                    </span>
                                                </td>
                                                <td>
                                                    <a href="villas/modifier.php?id=<?= $villa['id'] ?>" class="btn btn-warning btn-sm">
                                                        <i class="fas fa-edit"></i>
                                                    </a>
                                                </td>
                                            </tr>
                                        <?php endforeach; ?>
                                    </tbody>
                                </table>
                            </div>
                        <?php endif; ?>
                    </div>
                    
                    <!-- Actions rapides -->
                    <div class="glass-card fade-in-up" style="animation-delay: 0.2s;">
                        <div class="card-header">
                            <h3 class="card-title"><i class="fas fa-bolt"></i> Actions Rapides</h3>
                        </div>
                        
                        <div style="display: flex; flex-direction: column; gap: 1rem;">
                            <a href="villas/ajouter.php" class="btn btn-success" style="justify-content: flex-start;">
                                <i class="fas fa-plus"></i> Ajouter une villa
                            </a>
                            
                            <a href="images/upload.php" class="btn btn-primary" style="justify-content: flex-start;">
                                <i class="fas fa-upload"></i> Upload images
                            </a>
                            
                            <button onclick="generateAllPages()" class="btn btn-generate" style="justify-content: flex-start; width: 100%; border: none;">
                                <i class="fas fa-wand-magic-sparkles"></i> Générer Toutes les Pages
                            </button>

                            <!-- Progression génération -->
                            <div id="generation-progress" class="generation-progress">
                                <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>
                                <div id="progress-text" class="progress-text">Préparation...</div>
                            </div>
                            
                            <div id="generation-results" class="generation-results"></div>
                            
                            <a href="images/galerie.php" class="btn btn-primary" style="justify-content: flex-start;">
                                <i class="fas fa-images"></i> Gérer galerie
                            </a>
                            
                            <a href="api/villas.php" class="btn btn-primary" style="justify-content: flex-start;" target="_blank">
                                <i class="fas fa-code"></i> Voir API JSON
                            </a>
                            
                            <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.15); margin: 0.5rem 0;">
                            
                            <a href="../villas.html" class="btn btn-primary" style="justify-content: flex-start;" target="_blank">
                                <i class="fas fa-external-link-alt"></i> Page Villas
                            </a>
                            
                            <a href="../" class="btn btn-primary" style="justify-content: flex-start;" target="_blank">
                                <i class="fas fa-home"></i> Voir site web
                            </a>
                        </div>
                        
                        <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.15);">
                            <h4 style="color: white; font-size: 1rem; margin-bottom: 1rem;">
                                <i class="fas fa-info-circle"></i> Informations
                            </h4>
                            <div style="font-size: 0.85rem; color: rgba(255,255,255,0.8); line-height: 1.5;">
                                <p><strong>Version:</strong> 1.0.0</p>
                                <p><strong>Dernière maj:</strong> <?= date('d/m/Y H:i') ?></p>
                                <p><strong>Utilisateur:</strong> <?= sanitizeHtml($currentUser['nom']) ?></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    </div>
    
    <script src="assets/js/admin.js"></script>
    <script>
        // Affichage des résultats de génération
        function displayResults(result) {
            const container = document.getElementById('generation-results');
            container.style.display = 'block';
            const total = result?.total_generated || 0;
            const errors = result?.errors || [];
            let html = `<div><strong>${total}</strong> page(s) générée(s).</div>`;
            if (Array.isArray(result.generated) && result.generated.length) {
                html += '<ul>' + result.generated.slice(0,5).map(r => `<li>✅ ${r.villa_name} → <a href="../${r.filename}" target="_blank">${r.filename}</a></li>`).join('') + (result.generated.length > 5 ? '<li>…</li>' : '') + '</ul>';
            }
            if (errors.length) {
                html += `<div style="margin-top: .5rem; color: #ffb3b3;">${errors.length} erreur(s):</div>`;
                html += '<ul>' + errors.slice(0,5).map(e => `<li>❌ Villa #${e.villa_id}: ${e.error}</li>`).join('') + (errors.length > 5 ? '<li>…</li>' : '') + '</ul>';
            }
            container.innerHTML = html;
        }
    </script>
</body>
</html>