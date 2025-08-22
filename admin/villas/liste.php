<?php
/**
 * Liste des villas - KhanelConcept Admin
 */

require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

// Vérifier l'authentification
requireAuth();

$villaManager = new VillaManager();
$currentUser = getCurrentUser();

// Paramètres de filtrage et pagination
$page = isset($_GET['page']) ? max(1, (int)$_GET['page']) : 1;
$limit = 20;
$offset = ($page - 1) * $limit;

$filtersApplied = false;
$whereConditions = [];
$params = [];

// Filtres
$typeFilter = $_GET['type'] ?? '';
$statutFilter = $_GET['statut'] ?? '';
$locationFilter = $_GET['location'] ?? '';
$searchFilter = trim($_GET['search'] ?? '');

if ($typeFilter) {
    $whereConditions[] = "v.type = ?";
    $params[] = $typeFilter;
    $filtersApplied = true;
}

if ($statutFilter) {
    $whereConditions[] = "v.statut = ?";
    $params[] = $statutFilter;
    $filtersApplied = true;
}

if ($locationFilter) {
    $whereConditions[] = "v.localisation LIKE ?";
    $params[] = "%$locationFilter%";
    $filtersApplied = true;
}

if ($searchFilter) {
    $whereConditions[] = "(v.nom LIKE ? OR v.description LIKE ?)";
    $params[] = "%$searchFilter%";
    $params[] = "%$searchFilter%";
    $filtersApplied = true;
}

// Construction de la requête
$sql = "SELECT v.*, 
               (SELECT vi.nom_fichier FROM villa_images vi 
                WHERE vi.villa_id = v.id AND vi.image_principale = 1 
                LIMIT 1) as image_principale,
               (SELECT COUNT(*) FROM villa_images vi2 
                WHERE vi2.villa_id = v.id) as total_images
        FROM villas v";

if (!empty($whereConditions)) {
    $sql .= " WHERE " . implode(" AND ", $whereConditions);
}

$sql .= " ORDER BY v.created_at DESC";

// Compter le total
$countSql = "SELECT COUNT(*) as total FROM villas v";
if (!empty($whereConditions)) {
    $countSql .= " WHERE " . implode(" AND ", $whereConditions);
}

$totalResult = $db->query($countSql, $params);
$totalVillas = $totalResult->fetch()['total'];
$totalPages = ceil($totalVillas / $limit);

// Récupérer les villas paginées
$sql .= " LIMIT $limit OFFSET $offset";
$villas = $db->query($sql, $params)->fetchAll();

// Traitement des actions rapides (toggle statut)
if (isset($_POST['toggle_statut']) && isset($_POST['villa_id'])) {
    $villaId = (int)$_POST['villa_id'];
    $villa = $villaManager->getVillaById($villaId);
    
    if ($villa) {
        $nouveauStatut = match($villa['statut']) {
            'disponible' => 'indisponible',
            'indisponible' => 'maintenance',
            'maintenance' => 'disponible',
            default => 'disponible'
        };
        
        $villaManager->updateVilla($villaId, array_merge($villa, ['statut' => $nouveauStatut]));
        redirect('liste.php', "Statut modifié avec succès pour {$villa['nom']}");
    }
}

// Options pour les filtres
$types = ['F3', 'F5', 'F6', 'F7', 'Studio', 'Appartement', 'Espace'];
$statuts = ['disponible', 'indisponible', 'maintenance'];
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Liste des Villas - KhanelConcept Admin</title>
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
                <li><a href="liste.php" class="active"><i class="fas fa-home"></i> Villas</a></li>
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
                    <h2><i class="fas fa-home"></i> Liste des Villas</h2>
                    <p>Gérez toutes vos propriétés de location</p>
                </div>
                <div class="header-actions">
                    <a href="ajouter.php" class="btn btn-success">
                        <i class="fas fa-plus"></i> Ajouter une villa
                    </a>
                </div>
            </header>
            
            <!-- Zone de contenu -->
            <div class="content-area">
                <?php displayFlashMessage(); ?>
                
                <!-- Filtres -->
                <div class="glass-card">
                    <div class="card-header">
                        <h3 class="card-title"><i class="fas fa-filter"></i> Filtres & Recherche</h3>
                        <?php if ($filtersApplied): ?>
                            <a href="liste.php" class="btn btn-warning btn-sm">
                                <i class="fas fa-times"></i> Réinitialiser
                            </a>
                        <?php endif; ?>
                    </div>
                    
                    <form method="GET" action="" class="filters-form">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                            <div class="form-group">
                                <label for="search" class="form-label">Recherche</label>
                                <input type="text" id="search" name="search" class="form-control" 
                                       placeholder="Nom ou description..." value="<?= sanitizeHtml($searchFilter) ?>">
                            </div>
                            
                            <div class="form-group">
                                <label for="type" class="form-label">Type</label>
                                <select id="type" name="type" class="form-control">
                                    <option value="">Tous les types</option>
                                    <?php foreach ($types as $type): ?>
                                        <option value="<?= $type ?>" <?= $typeFilter === $type ? 'selected' : '' ?>>
                                            <?= $type ?>
                                        </option>
                                    <?php endforeach; ?>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="statut" class="form-label">Statut</label>
                                <select id="statut" name="statut" class="form-control">
                                    <option value="">Tous les statuts</option>
                                    <?php foreach ($statuts as $statut): ?>
                                        <option value="<?= $statut ?>" <?= $statutFilter === $statut ? 'selected' : '' ?>>
                                            <?= ucfirst($statut) ?>
                                        </option>
                                    <?php endforeach; ?>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="location" class="form-label">Localisation</label>
                                <input type="text" id="location" name="location" class="form-control" 
                                       placeholder="Ville, région..." value="<?= sanitizeHtml($locationFilter) ?>">
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 1rem;">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-search"></i> Filtrer
                            </button>
                            
                            <?php if ($filtersApplied): ?>
                                <a href="liste.php" class="btn btn-warning">
                                    <i class="fas fa-times"></i> Réinitialiser
                                </a>
                            <?php endif; ?>
                        </div>
                    </form>
                </div>
                
                <!-- Résultats -->
                <div class="glass-card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-list"></i> 
                            <?= $totalVillas ?> villa(s) trouvée(s)
                            <?php if ($filtersApplied): ?>
                                <span style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">(filtré)</span>
                            <?php endif; ?>
                        </h3>
                        
                        <div style="display: flex; gap: 1rem; align-items: center;">
                            <?php if ($totalPages > 1): ?>
                                <span style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">
                                    Page <?= $page ?>/<?= $totalPages ?>
                                </span>
                            <?php endif; ?>
                            
                            <a href="../images/upload.php" class="btn btn-primary btn-sm">
                                <i class="fas fa-upload"></i> Upload Images
                            </a>
                        </div>
                    </div>
                    
                    <?php if (empty($villas)): ?>
                        <div style="text-align: center; padding: 3rem; color: rgba(255,255,255,0.7);">
                            <i class="fas fa-home" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.3;"></i>
                            <h3>Aucune villa trouvée</h3>
                            <p>
                                <?php if ($filtersApplied): ?>
                                    Aucune villa ne correspond à vos critères de recherche.
                                <?php else: ?>
                                    Vous n'avez pas encore ajouté de villa.
                                <?php endif; ?>
                            </p>
                            <div style="margin-top: 2rem;">
                                <?php if ($filtersApplied): ?>
                                    <a href="liste.php" class="btn btn-warning">
                                        <i class="fas fa-times"></i> Réinitialiser les filtres
                                    </a>
                                <?php endif; ?>
                                <a href="ajouter.php" class="btn btn-success">
                                    <i class="fas fa-plus"></i> Ajouter une villa
                                </a>
                            </div>
                        </div>
                    <?php else: ?>
                        <div class="table-responsive">
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th style="width: 80px;">Image</th>
                                        <th>Villa</th>
                                        <th style="width: 100px;">Type</th>
                                        <th style="width: 120px;">Prix/Nuit</th>
                                        <th style="width: 80px;">Capacité</th>
                                        <th style="width: 100px;">Statut</th>
                                        <th style="width: 80px;">Images</th>
                                        <th style="width: 150px;">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <?php foreach ($villas as $villa): ?>
                                        <tr>
                                            <td>
                                                <?php if ($villa['image_principale']): ?>
                                                    <img src="<?= UPLOAD_URL . $villa['image_principale'] ?>" 
                                                         alt="<?= sanitizeHtml($villa['nom']) ?>" 
                                                         class="table-image"
                                                         onclick="previewImage('<?= UPLOAD_URL . $villa['image_principale'] ?>', '<?= sanitizeHtml($villa['nom']) ?>')">
                                                <?php else: ?>
                                                    <div class="table-image" style="background: rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: center;">
                                                        <i class="fas fa-image" style="color: rgba(255,255,255,0.5);"></i>
                                                    </div>
                                                <?php endif; ?>
                                            </td>
                                            
                                            <td>
                                                <div>
                                                    <strong><?= sanitizeHtml($villa['nom']) ?></strong>
                                                    <?php if ($villa['featured']): ?>
                                                        <i class="fas fa-star" style="color: #ffc107; margin-left: 0.5rem;" title="Villa vedette"></i>
                                                    <?php endif; ?>
                                                </div>
                                                <div style="font-size: 0.8rem; opacity: 0.8; margin-top: 0.25rem;">
                                                    <i class="fas fa-map-marker-alt"></i> 
                                                    <?= sanitizeHtml($villa['localisation']) ?>
                                                </div>
                                                <div style="font-size: 0.75rem; opacity: 0.6; margin-top: 0.25rem;">
                                                    <?= sanitizeHtml($villa['slug']) ?>
                                                </div>
                                            </td>
                                            
                                            <td>
                                                <span class="badge badge-success" style="background: rgba(255,255,255,0.15);">
                                                    <?= sanitizeHtml($villa['type']) ?>
                                                </span>
                                            </td>
                                            
                                            <td style="font-weight: 600; color: #ffc107;">
                                                <?= formatPrice($villa['prix_nuit']) ?>
                                            </td>
                                            
                                            <td>
                                                <div style="font-size: 0.9rem;">
                                                    <i class="fas fa-users"></i> <?= $villa['capacite_max'] ?>
                                                </div>
                                                <div style="font-size: 0.75rem; opacity: 0.7;">
                                                    <?= $villa['nombre_chambres'] ?>ch • <?= $villa['nombre_salles_bain'] ?>sdb
                                                </div>
                                            </td>
                                            
                                            <td>
                                                <form method="POST" style="display: inline;">
                                                    <input type="hidden" name="villa_id" value="<?= $villa['id'] ?>">
                                                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                                                    
                                                    <button type="submit" name="toggle_statut" class="badge <?= 
                                                        match($villa['statut']) {
                                                            'disponible' => 'badge-success',
                                                            'indisponible' => 'badge-danger', 
                                                            'maintenance' => 'badge-warning',
                                                            default => 'badge-success'
                                                        }
                                                    ?>" style="border: none; cursor: pointer;" 
                                                            title="Cliquer pour changer le statut">
                                                        <?= ucfirst($villa['statut']) ?>
                                                    </button>
                                                </form>
                                            </td>
                                            
                                            <td>
                                                <div style="font-size: 0.9rem;">
                                                    <i class="fas fa-images"></i> <?= $villa['total_images'] ?>
                                                    <?php if ($villa['image_principale']): ?>
                                                        <i class="fas fa-star" style="color: #ffc107; font-size: 0.7rem; margin-left: 0.25rem;" title="Image principale définie"></i>
                                                    <?php endif; ?>
                                                </div>
                                            </td>
                                            
                                            <td>
                                                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                                    <a href="modifier.php?id=<?= $villa['id'] ?>" class="btn btn-warning btn-sm" title="Modifier">
                                                        <i class="fas fa-edit"></i>
                                                    </a>
                                                    
                                                    <a href="../images/upload.php?villa_id=<?= $villa['id'] ?>" class="btn btn-primary btn-sm" title="Gérer images">
                                                        <i class="fas fa-images"></i>
                                                    </a>
                                                    
                                                    <a href="supprimer.php?id=<?= $villa['id'] ?>" class="btn btn-danger btn-sm" 
                                                       onclick="return confirm('Êtes-vous sûr de vouloir supprimer cette villa ? Cette action est irréversible.')"
                                                       title="Supprimer">
                                                        <i class="fas fa-trash"></i>
                                                    </a>
                                                </div>
                                            </td>
                                        </tr>
                                    <?php endforeach; ?>
                                </tbody>
                            </table>
                        </div>
                        
                        <!-- Pagination -->
                        <?php if ($totalPages > 1): ?>
                            <div style="display: flex; justify-content: center; margin-top: 2rem; gap: 0.5rem;">
                                <?php if ($page > 1): ?>
                                    <a href="?page=<?= $page - 1 ?><?= $filtersApplied ? '&' . http_build_query($_GET) : '' ?>" 
                                       class="btn btn-primary btn-sm">
                                        <i class="fas fa-chevron-left"></i> Précédent
                                    </a>
                                <?php endif; ?>
                                
                                <?php 
                                $start = max(1, $page - 2);
                                $end = min($totalPages, $page + 2);
                                ?>
                                
                                <?php for ($i = $start; $i <= $end; $i++): ?>
                                    <?php if ($i === $page): ?>
                                        <span class="btn btn-success btn-sm"><?= $i ?></span>
                                    <?php else: ?>
                                        <a href="?page=<?= $i ?><?= $filtersApplied ? '&' . http_build_query(array_merge($_GET, ['page' => $i])) : '' ?>" 
                                           class="btn btn-primary btn-sm">
                                            <?= $i ?>
                                        </a>
                                    <?php endif; ?>
                                <?php endfor; ?>
                                
                                <?php if ($page < $totalPages): ?>
                                    <a href="?page=<?= $page + 1 ?><?= $filtersApplied ? '&' . http_build_query(array_merge($_GET, ['page' => $page + 1])) : '' ?>" 
                                       class="btn btn-primary btn-sm">
                                        Suivant <i class="fas fa-chevron-right"></i>
                                    </a>
                                <?php endif; ?>
                            </div>
                        <?php endif; ?>
                    <?php endif; ?>
                </div>
            </div>
        </main>
    </div>
    
    <!-- Modal de prévisualisation -->
    <div id="imageModal" class="image-modal" style="display: none;">
        <div class="modal-backdrop" onclick="closeImageModal()"></div>
        <div class="modal-content">
            <button onclick="closeImageModal()" class="modal-close">
                <i class="fas fa-times"></i>
            </button>
            <img id="modalImage" src="" alt="" style="max-width: 90vw; max-height: 90vh; border-radius: 8px;">
            <div id="modalTitle" style="text-align: center; margin-top: 1rem; color: white; font-weight: 600;"></div>
        </div>
    </div>
    
    <script src="../assets/js/admin.js"></script>
    <script>
        // Modal de prévisualisation d'image
        function previewImage(src, title) {
            document.getElementById('modalImage').src = src;
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('imageModal').style.display = 'flex';
        }
        
        function closeImageModal() {
            document.getElementById('imageModal').style.display = 'none';
        }
        
        // Styles pour la modal
        document.head.insertAdjacentHTML('beforeend', `
            <style>
                .image-modal {
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
                    top: -40px;
                    right: 0;
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    border: none;
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 1.2rem;
                }
                
                .table-image {
                    cursor: pointer;
                    transition: transform 0.2s ease;
                }
                
                .table-image:hover {
                    transform: scale(1.05);
                }
            </style>
        `);
        
        // Auto-submit des filtres avec debounce
        let filterTimeout;
        document.querySelectorAll('#search, #location').forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(filterTimeout);
                filterTimeout = setTimeout(() => {
                    this.closest('form').submit();
                }, 1000);
            });
        });
        
        // Submit immédiat pour les selects
        document.querySelectorAll('#type, #statut').forEach(select => {
            select.addEventListener('change', function() {
                this.closest('form').submit();
            });
        });
    </script>
</body>
</html>