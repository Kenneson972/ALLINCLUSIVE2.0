<?php
/**
 * Ajouter une villa - KhanelConcept Admin
 */

require_once '../includes/config.php';
require_once '../includes/auth.php';
require_once '../includes/functions.php';

// Vérifier l'authentification
requireAuth();

$villaManager = new VillaManager();
$currentUser = getCurrentUser();

// Équipements disponibles
$equipementsDisponibles = [
    'Piscine', 'WiFi', 'Climatisation', 'Jacuzzi', 'Vue mer', 'Vue montagne',
    'Terrasse', 'Jardin', 'Parking', 'Cuisine équipée', 'Barbecue', 'Lave-linge',
    'Lave-vaisselle', 'Télévision', 'Balcon', 'Proche plage', 'Calme', 'Animaux acceptés'
];

$errors = [];
$formData = [];

// Traitement du formulaire
if ($_POST && isset($_POST['ajouter_villa'])) {
    // Vérifier le token CSRF
    if (!validateCSRFToken($_POST['csrf_token'] ?? '')) {
        $errors[] = 'Token de sécurité invalide.';
    } else {
        // Récupérer et valider les données
        $formData = [
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
        
        // Générer le slug
        $baseSlug = generateSlug($formData['nom']);
        $formData['slug'] = $baseSlug;
        
        // Vérifier l'unicité du slug
        $counter = 1;
        while (!$villaManager->isSlugUnique($formData['slug'])) {
            $formData['slug'] = $baseSlug . '-' . $counter;
            $counter++;
        }
        
        // Validations
        if (empty($formData['nom'])) {
            $errors[] = 'Le nom de la villa est obligatoire.';
        } elseif (strlen($formData['nom']) < 3) {
            $errors[] = 'Le nom doit contenir au moins 3 caractères.';
        }
        
        if (empty($formData['type'])) {
            $errors[] = 'Le type de villa est obligatoire.';
        } elseif (!in_array($formData['type'], ['F3', 'F5', 'F6', 'F7', 'Studio', 'Appartement', 'Espace'])) {
            $errors[] = 'Type de villa invalide.';
        }
        
        if (empty($formData['localisation'])) {
            $errors[] = 'La localisation est obligatoire.';
        }
        
        if (empty($formData['prix_nuit']) || !is_numeric($formData['prix_nuit']) || $formData['prix_nuit'] <= 0) {
            $errors[] = 'Le prix par nuit doit être un nombre positif.';
        }
        
        if (empty($formData['capacite_max']) || !is_numeric($formData['capacite_max']) || $formData['capacite_max'] <= 0) {
            $errors[] = 'La capacité maximale doit être un nombre entier positif.';
        }
        
        if (empty($formData['nombre_chambres']) || !is_numeric($formData['nombre_chambres']) || $formData['nombre_chambres'] < 0) {
            $errors[] = 'Le nombre de chambres doit être un nombre entier positif ou nul.';
        }
        
        if (empty($formData['nombre_salles_bain']) || !is_numeric($formData['nombre_salles_bain']) || $formData['nombre_salles_bain'] < 0) {
            $errors[] = 'Le nombre de salles de bain doit être un nombre entier positif ou nul.';
        }
        
        if (!in_array($formData['statut'], ['disponible', 'indisponible', 'maintenance'])) {
            $errors[] = 'Statut invalide.';
        }
        
        // Si pas d'erreurs, créer la villa
        if (empty($errors)) {
            $villaId = $villaManager->createVilla($formData);
            
            if ($villaId) {
                redirect('modifier.php?id=' . $villaId, 'Villa créée avec succès ! Vous pouvez maintenant ajouter des images.');
            } else {
                $errors[] = 'Erreur lors de la création de la villa.';
            }
        }
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ajouter une Villa - KhanelConcept Admin</title>
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
                <li><a href="liste.php"><i class="fas fa-home"></i> Villas</a></li>
                <li><a href="ajouter.php" class="active"><i class="fas fa-plus"></i> Ajouter Villa</a></li>
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
                    <h2><i class="fas fa-plus"></i> Ajouter une Villa</h2>
                    <p>Créer une nouvelle propriété de location</p>
                </div>
                <div class="header-actions">
                    <a href="liste.php" class="btn btn-primary">
                        <i class="fas fa-list"></i> Retour à la liste
                    </a>
                </div>
            </header>
            
            <!-- Zone de contenu -->
            <div class="content-area">
                <?php displayFlashMessage(); ?>
                
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
                
                <form method="POST" action="" class="villa-form" data-validate>
                    <input type="hidden" name="csrf_token" value="<?= generateCSRFToken() ?>">
                    
                    <div class="glass-card">
                        <div class="card-header">
                            <h3 class="card-title"><i class="fas fa-info-circle"></i> Informations Générales</h3>
                        </div>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="nom" class="form-label">
                                    <i class="fas fa-home"></i> Nom de la villa *
                                </label>
                                <input type="text" id="nom" name="nom" class="form-control" 
                                       placeholder="Ex: Villa F3 sur Petit Macabou"
                                       value="<?= sanitizeHtml($formData['nom'] ?? '') ?>" 
                                       required>
                                <div class="form-help">Le slug sera généré automatiquement</div>
                            </div>
                            
                            <div class="form-group">
                                <label for="slug" class="form-label">
                                    <i class="fas fa-link"></i> Slug (URL)
                                </label>
                                <input type="text" id="slug" name="slug" class="form-control" 
                                       placeholder="villa-f3-petit-macabou"
                                       value="<?= sanitizeHtml($formData['slug'] ?? '') ?>" 
                                       readonly>
                                <div class="form-help">URL de la page villa (généré automatiquement)</div>
                            </div>
                            
                            <div class="form-group">
                                <label for="type" class="form-label">
                                    <i class="fas fa-building"></i> Type de villa *
                                </label>
                                <select id="type" name="type" class="form-control" required>
                                    <option value="">Sélectionner un type</option>
                                    <option value="F3" <?= ($formData['type'] ?? '') === 'F3' ? 'selected' : '' ?>>F3</option>
                                    <option value="F5" <?= ($formData['type'] ?? '') === 'F5' ? 'selected' : '' ?>>F5</option>
                                    <option value="F6" <?= ($formData['type'] ?? '') === 'F6' ? 'selected' : '' ?>>F6</option>
                                    <option value="F7" <?= ($formData['type'] ?? '') === 'F7' ? 'selected' : '' ?>>F7</option>
                                    <option value="Studio" <?= ($formData['type'] ?? '') === 'Studio' ? 'selected' : '' ?>>Studio</option>
                                    <option value="Appartement" <?= ($formData['type'] ?? '') === 'Appartement' ? 'selected' : '' ?>>Appartement</option>
                                    <option value="Espace" <?= ($formData['type'] ?? '') === 'Espace' ? 'selected' : '' ?>>Espace</option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label for="localisation" class="form-label">
                                    <i class="fas fa-map-marker-alt"></i> Localisation *
                                </label>
                                <input type="text" id="localisation" name="localisation" class="form-control" 
                                       placeholder="Ex: Petit Macabou, Vauclin"
                                       value="<?= sanitizeHtml($formData['localisation'] ?? '') ?>" 
                                       required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="glass-card">
                        <div class="card-header">
                            <h3 class="card-title"><i class="fas fa-euro-sign"></i> Tarification & Capacité</h3>
                        </div>
                        
                        <div class="form-grid">
                            <div class="form-group">
                                <label for="prix_nuit" class="form-label">
                                    <i class="fas fa-euro-sign"></i> Prix par nuit (€) *
                                </label>
                                <input type="number" id="prix_nuit" name="prix_nuit" class="form-control" 
                                       placeholder="350"
                                       step="0.01" min="0"
                                       value="<?= sanitizeHtml($formData['prix_nuit'] ?? '') ?>" 
                                       required>
                            </div>
                            
                            <div class="form-group">
                                <label for="capacite_max" class="form-label">
                                    <i class="fas fa-users"></i> Capacité maximale *
                                </label>
                                <input type="number" id="capacite_max" name="capacite_max" class="form-control" 
                                       placeholder="6"
                                       min="1"
                                       value="<?= sanitizeHtml($formData['capacite_max'] ?? '') ?>" 
                                       required>
                            </div>
                            
                            <div class="form-group">
                                <label for="nombre_chambres" class="form-label">
                                    <i class="fas fa-bed"></i> Nombre de chambres *
                                </label>
                                <input type="number" id="nombre_chambres" name="nombre_chambres" class="form-control" 
                                       placeholder="3"
                                       min="0"
                                       value="<?= sanitizeHtml($formData['nombre_chambres'] ?? '') ?>" 
                                       required>
                            </div>
                            
                            <div class="form-group">
                                <label for="nombre_salles_bain" class="form-label">
                                    <i class="fas fa-bath"></i> Nombre de salles de bain *
                                </label>
                                <input type="number" id="nombre_salles_bain" name="nombre_salles_bain" class="form-control" 
                                       placeholder="2"
                                       min="0"
                                       value="<?= sanitizeHtml($formData['nombre_salles_bain'] ?? '') ?>" 
                                       required>
                            </div>
                        </div>
                    </div>
                    
                    <div class="glass-card">
                        <div class="card-header">
                            <h3 class="card-title"><i class="fas fa-list-check"></i> Équipements</h3>
                        </div>
                        
                        <div class="equipements-grid">
                            <?php foreach ($equipementsDisponibles as $equipement): ?>
                                <label class="equipement-item">
                                    <input type="checkbox" name="equipements[]" value="<?= sanitizeHtml($equipement) ?>"
                                           <?= in_array($equipement, $formData['equipements'] ?? []) ? 'checked' : '' ?>>
                                    <span class="equipement-label">
                                        <i class="fas fa-check"></i>
                                        <?= sanitizeHtml($equipement) ?>
                                    </span>
                                </label>
                            <?php endforeach; ?>
                        </div>
                    </div>
                    
                    <div class="glass-card">
                        <div class="card-header">
                            <h3 class="card-title"><i class="fas fa-edit"></i> Description & Caractéristiques</h3>
                        </div>
                        
                        <div class="form-group">
                            <label for="description" class="form-label">
                                <i class="fas fa-align-left"></i> Description
                            </label>
                            <textarea id="description" name="description" class="form-control" rows="4"
                                      placeholder="Description détaillée de la villa..."><?= sanitizeHtml($formData['description'] ?? '') ?></textarea>
                            <div class="form-help">Description qui apparaîtra sur la page de la villa</div>
                        </div>
                        
                        <div class="form-group">
                            <label for="caracteristiques" class="form-label">
                                <i class="fas fa-star"></i> Caractéristiques principales
                            </label>
                            <input type="text" id="caracteristiques" name="caracteristiques" class="form-control" 
                                   placeholder="Piscine, Vue mer, Terrasse, Climatisation"
                                   value="<?= sanitizeHtml($formData['caracteristiques'] ?? '') ?>">
                            <div class="form-help">Liste séparée par des virgules</div>
                        </div>
                    </div>
                    
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
                                    <option value="disponible" <?= ($formData['statut'] ?? 'disponible') === 'disponible' ? 'selected' : '' ?>>
                                        Disponible
                                    </option>
                                    <option value="indisponible" <?= ($formData['statut'] ?? '') === 'indisponible' ? 'selected' : '' ?>>
                                        Indisponible
                                    </option>
                                    <option value="maintenance" <?= ($formData['statut'] ?? '') === 'maintenance' ? 'selected' : '' ?>>
                                        En maintenance
                                    </option>
                                </select>
                            </div>
                            
                            <div class="form-group">
                                <label class="form-label">
                                    <i class="fas fa-star"></i> Options
                                </label>
                                <label class="checkbox-item">
                                    <input type="checkbox" name="featured" value="1" 
                                           <?= ($formData['featured'] ?? 0) ? 'checked' : '' ?>>
                                    <span class="checkbox-label">
                                        <i class="fas fa-star"></i>
                                        Villa en vedette
                                    </span>
                                </label>
                                <div class="form-help">Sera mise en avant sur le site</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-actions">
                        <button type="submit" name="ajouter_villa" class="btn btn-success">
                            <i class="fas fa-save"></i> Créer la villa
                        </button>
                        
                        <a href="liste.php" class="btn btn-warning">
                            <i class="fas fa-times"></i> Annuler
                        </a>
                        
                        <button type="reset" class="btn btn-primary">
                            <i class="fas fa-undo"></i> Réinitialiser
                        </button>
                    </div>
                </form>
            </div>
        </main>
    </div>
    
    <script src="../assets/js/admin.js"></script>
    <script>
        // Auto-génération du slug
        document.getElementById('nom').addEventListener('input', function() {
            const slug = AdminPanel.generateSlug(this.value);
            document.getElementById('slug').value = slug;
        });
        
        // Preview du prix formaté
        document.getElementById('prix_nuit').addEventListener('input', function() {
            const prix = parseFloat(this.value);
            if (!isNaN(prix)) {
                // Optionnel: afficher le prix formaté
                console.log('Prix:', AdminPanel.formatPrice(prix));
            }
        });
        
        // Validation en temps réel
        document.querySelectorAll('input[required], select[required]').forEach(field => {
            field.addEventListener('blur', function() {
                if (!this.value.trim()) {
                    this.style.borderColor = '#dc3545';
                } else {
                    this.style.borderColor = '';
                }
            });
        });
        
        // Confirmation avant reset
        document.querySelector('button[type="reset"]').addEventListener('click', function(e) {
            if (!confirm('Êtes-vous sûr de vouloir réinitialiser tous les champs ?')) {
                e.preventDefault();
            }
        });
    </script>
    
    <style>
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
        
        .form-actions {
            display: flex;
            gap: 1rem;
            justify-content: flex-start;
            margin-top: 2rem;
        }
        
        @media (max-width: 768px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            
            .equipements-grid {
                grid-template-columns: 1fr;
            }
            
            .form-actions {
                flex-direction: column;
            }
        }
    </style>
</body>
</html>