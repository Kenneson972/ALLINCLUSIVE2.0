<?php
/**
 * Fonctions utilitaires - KhanelConcept Admin
 */

require_once 'config.php';

/**
 * Classe Villa - Gestion des villas
 */
class VillaManager {
    private $db;
    
    public function __construct() {
        $this->db = Database::getInstance();
    }
    
    /**
     * Obtenir toutes les villas
     */
    public function getAllVillas($statut = null) {
        $sql = "SELECT v.*, 
                       (SELECT vi.nom_fichier FROM villa_images vi 
                        WHERE vi.villa_id = v.id AND vi.image_principale = 1 
                        LIMIT 1) as image_principale
                FROM villas v";
        
        $params = [];
        if ($statut) {
            $sql .= " WHERE v.statut = ?";
            $params[] = $statut;
        }
        
        $sql .= " ORDER BY v.created_at DESC";
        
        return $this->db->query($sql, $params)->fetchAll();
    }
    
    /**
     * Obtenir une villa par ID
     */
    public function getVillaById($id) {
        $sql = "SELECT * FROM villas WHERE id = ?";
        $villa = $this->db->query($sql, [$id])->fetch();
        
        if ($villa) {
            // Récupérer les images
            $villa['images'] = $this->getVillaImages($id);
        }
        
        return $villa;
    }
    
    /**
     * Obtenir une villa par slug
     */
    public function getVillaBySlug($slug) {
        $sql = "SELECT * FROM villas WHERE slug = ?";
        $villa = $this->db->query($sql, [$slug])->fetch();
        
        if ($villa) {
            $villa['images'] = $this->getVillaImages($villa['id']);
        }
        
        return $villa;
    }
    
    /**
     * Créer une nouvelle villa
     */
    public function createVilla($data) {
        try {
            $sql = "INSERT INTO villas (nom, slug, type, localisation, prix_nuit, capacite_max, 
                    nombre_chambres, nombre_salles_bain, description, caracteristiques, equipements, statut, featured) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            
            $equipements = isset($data['equipements']) ? json_encode($data['equipements']) : null;
            
            $this->db->query($sql, [
                $data['nom'],
                $data['slug'],
                $data['type'],
                $data['localisation'],
                $data['prix_nuit'],
                $data['capacite_max'],
                $data['nombre_chambres'],
                $data['nombre_salles_bain'],
                $data['description'],
                $data['caracteristiques'],
                $equipements,
                $data['statut'] ?? 'disponible',
                $data['featured'] ?? 0
            ]);
            
            return $this->db->lastInsertId();
            
        } catch (Exception $e) {
            error_log("Erreur création villa : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Mettre à jour une villa
     */
    public function updateVilla($id, $data) {
        try {
            $sql = "UPDATE villas SET nom = ?, slug = ?, type = ?, localisation = ?, prix_nuit = ?, 
                    capacite_max = ?, nombre_chambres = ?, nombre_salles_bain = ?, description = ?, 
                    caracteristiques = ?, equipements = ?, statut = ?, featured = ?, updated_at = NOW() 
                    WHERE id = ?";
            
            $equipements = isset($data['equipements']) ? json_encode($data['equipements']) : null;
            
            $result = $this->db->query($sql, [
                $data['nom'],
                $data['slug'],
                $data['type'],
                $data['localisation'],
                $data['prix_nuit'],
                $data['capacite_max'],
                $data['nombre_chambres'],
                $data['nombre_salles_bain'],
                $data['description'],
                $data['caracteristiques'],
                $equipements,
                $data['statut'] ?? 'disponible',
                $data['featured'] ?? 0,
                $id
            ]);
            
            return $result->rowCount() > 0;
            
        } catch (Exception $e) {
            error_log("Erreur mise à jour villa : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Supprimer une villa
     */
    public function deleteVilla($id) {
        try {
            // Supprimer d'abord les images physiques
            $images = $this->getVillaImages($id);
            foreach ($images as $image) {
                $filePath = UPLOAD_PATH . $image['nom_fichier'];
                if (file_exists($filePath)) {
                    unlink($filePath);
                }
            }
            
            // La suppression en BDD se fait automatiquement via CASCADE
            $sql = "DELETE FROM villas WHERE id = ?";
            $result = $this->db->query($sql, [$id]);
            
            return $result->rowCount() > 0;
            
        } catch (Exception $e) {
            error_log("Erreur suppression villa : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Obtenir les images d'une villa
     */
    public function getVillaImages($villaId) {
        $sql = "SELECT * FROM villa_images WHERE villa_id = ? ORDER BY ordre_affichage ASC, id ASC";
        return $this->db->query($sql, [$villaId])->fetchAll();
    }
    
    /**
     * Ajouter une image à une villa
     */
    public function addVillaImage($villaId, $nomFichier, $nomOriginal, $altText = '', $imagePrincipale = false) {
        try {
            // Si c'est l'image principale, retirer le statut des autres
            if ($imagePrincipale) {
                $sql = "UPDATE villa_images SET image_principale = 0 WHERE villa_id = ?";
                $this->db->query($sql, [$villaId]);
            }
            
            $sql = "INSERT INTO villa_images (villa_id, nom_fichier, nom_original, alt_text, image_principale) 
                    VALUES (?, ?, ?, ?, ?)";
            
            $this->db->query($sql, [$villaId, $nomFichier, $nomOriginal, $altText, $imagePrincipale ? 1 : 0]);
            
            return $this->db->lastInsertId();
            
        } catch (Exception $e) {
            error_log("Erreur ajout image : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Supprimer une image
     */
    public function deleteImage($imageId) {
        try {
            // Récupérer les infos de l'image
            $sql = "SELECT * FROM villa_images WHERE id = ?";
            $image = $this->db->query($sql, [$imageId])->fetch();
            
            if ($image) {
                // Supprimer le fichier physique
                $filePath = UPLOAD_PATH . $image['nom_fichier'];
                if (file_exists($filePath)) {
                    unlink($filePath);
                }
                
                // Supprimer en BDD
                $sql = "DELETE FROM villa_images WHERE id = ?";
                $this->db->query($sql, [$imageId]);
                
                return true;
            }
            
            return false;
            
        } catch (Exception $e) {
            error_log("Erreur suppression image : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Définir une image comme principale
     */
    public function setMainImage($villaId, $imageId) {
        try {
            // Retirer le statut principal de toutes les images
            $sql = "UPDATE villa_images SET image_principale = 0 WHERE villa_id = ?";
            $this->db->query($sql, [$villaId]);
            
            // Définir la nouvelle image principale
            $sql = "UPDATE villa_images SET image_principale = 1 WHERE id = ? AND villa_id = ?";
            $result = $this->db->query($sql, [$imageId, $villaId]);
            
            return $result->rowCount() > 0;
            
        } catch (Exception $e) {
            error_log("Erreur définition image principale : " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Obtenir les statistiques du dashboard
     */
    public function getDashboardStats() {
        $stats = [];
        
        // Total villas
        $sql = "SELECT COUNT(*) as total FROM villas";
        $stats['total_villas'] = $this->db->query($sql)->fetch()['total'];
        
        // Villas disponibles
        $sql = "SELECT COUNT(*) as disponibles FROM villas WHERE statut = 'disponible'";
        $stats['villas_disponibles'] = $this->db->query($sql)->fetch()['disponibles'];
        
        // Villas indisponibles
        $sql = "SELECT COUNT(*) as indisponibles FROM villas WHERE statut = 'indisponible'";
        $stats['villas_indisponibles'] = $this->db->query($sql)->fetch()['indisponibles'];
        
        // Total images
        $sql = "SELECT COUNT(*) as total_images FROM villa_images";
        $stats['total_images'] = $this->db->query($sql)->fetch()['total_images'];
        
        // Villas featured
        $sql = "SELECT COUNT(*) as featured FROM villas WHERE featured = 1";
        $stats['villas_featured'] = $this->db->query($sql)->fetch()['featured'];
        
        return $stats;
    }
    
    /**
     * Vérifier si un slug est unique
     */
    public function isSlugUnique($slug, $excludeId = null) {
        $sql = "SELECT COUNT(*) as count FROM villas WHERE slug = ?";
        $params = [$slug];
        
        if ($excludeId) {
            $sql .= " AND id != ?";
            $params[] = $excludeId;
        }
        
        $result = $this->db->query($sql, $params)->fetch();
        return $result['count'] == 0;
    }
}

/**
 * Classe Upload - Gestion des uploads d'images
 */
class ImageUploader {
    
    /**
     * Uploader une image
     */
    public static function upload($file, $prefix = 'villa_') {
        try {
            // Vérifications de base
            if (!isset($file['error']) || $file['error'] !== UPLOAD_ERR_OK) {
                throw new Exception('Erreur lors de l\'upload du fichier');
            }
            
            if ($file['size'] > MAX_UPLOAD_SIZE) {
                throw new Exception('Le fichier est trop volumineux (max 5MB)');
            }
            
            // Vérifier l'extension
            $extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
            if (!in_array($extension, ALLOWED_EXTENSIONS)) {
                throw new Exception('Format de fichier non autorisé');
            }
            
            // Vérifier que c'est vraiment une image
            $imageInfo = getimagesize($file['tmp_name']);
            if ($imageInfo === false) {
                throw new Exception('Le fichier n\'est pas une image valide');
            }
            
            // Générer un nom unique
            $fileName = $prefix . time() . '_' . uniqid() . '.' . $extension;
            $uploadPath = UPLOAD_PATH . $fileName;
            
            // Créer le dossier si nécessaire
            if (!is_dir(UPLOAD_PATH)) {
                mkdir(UPLOAD_PATH, 0755, true);
            }
            
            // Déplacer le fichier
            if (!move_uploaded_file($file['tmp_name'], $uploadPath)) {
                throw new Exception('Impossible de déplacer le fichier uploadé');
            }
            
            // Redimensionner si nécessaire
            self::resizeImage($uploadPath, $imageInfo);
            
            return [
                'success' => true,
                'fileName' => $fileName,
                'originalName' => $file['name'],
                'size' => filesize($uploadPath),
                'dimensions' => $imageInfo[0] . 'x' . $imageInfo[1]
            ];
            
        } catch (Exception $e) {
            return [
                'success' => false,
                'error' => $e->getMessage()
            ];
        }
    }
    
    /**
     * Redimensionner une image si nécessaire
     */
    private static function resizeImage($filePath, $imageInfo) {
        $width = $imageInfo[0];
        $height = $imageInfo[1];
        
        // Pas de redimensionnement nécessaire
        if ($width <= IMAGE_MAX_WIDTH && $height <= IMAGE_MAX_HEIGHT) {
            return;
        }
        
        // Calculer les nouvelles dimensions
        $ratio = min(IMAGE_MAX_WIDTH / $width, IMAGE_MAX_HEIGHT / $height);
        $newWidth = floor($width * $ratio);
        $newHeight = floor($height * $ratio);
        
        // Créer les ressources d'image
        $sourceImage = null;
        switch ($imageInfo[2]) {
            case IMAGETYPE_JPEG:
                $sourceImage = imagecreatefromjpeg($filePath);
                break;
            case IMAGETYPE_PNG:
                $sourceImage = imagecreatefrompng($filePath);
                break;
            case IMAGETYPE_WEBP:
                $sourceImage = imagecreatefromwebp($filePath);
                break;
        }
        
        if (!$sourceImage) return;
        
        // Créer la nouvelle image
        $newImage = imagecreatetruecolor($newWidth, $newHeight);
        
        // Préserver la transparence pour PNG
        if ($imageInfo[2] == IMAGETYPE_PNG) {
            imagealphablending($newImage, false);
            imagesavealpha($newImage, true);
        }
        
        // Redimensionner
        imagecopyresampled($newImage, $sourceImage, 0, 0, 0, 0, $newWidth, $newHeight, $width, $height);
        
        // Sauvegarder
        switch ($imageInfo[2]) {
            case IMAGETYPE_JPEG:
                imagejpeg($newImage, $filePath, 85);
                break;
            case IMAGETYPE_PNG:
                imagepng($newImage, $filePath, 8);
                break;
            case IMAGETYPE_WEBP:
                imagewebp($newImage, $filePath, 85);
                break;
        }
        
        // Libérer la mémoire
        imagedestroy($sourceImage);
        imagedestroy($newImage);
    }
}

/**
 * Formater la taille d'un fichier
 */
function formatFileSize($bytes) {
    if ($bytes === 0) return '0 B';
    
    $units = ['B', 'KB', 'MB', 'GB'];
    $factor = floor((strlen($bytes) - 1) / 3);
    
    return sprintf("%.1f", $bytes / pow(1024, $factor)) . ' ' . $units[$factor];
}

?>