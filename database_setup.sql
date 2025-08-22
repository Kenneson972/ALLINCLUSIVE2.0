-- ================================
-- SCRIPT SQL CREATION TABLES
-- KhanelConcept Admin Panel
-- ================================

-- 1. TABLE VILLAS (principale)
CREATE TABLE villas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    type ENUM('F3', 'F5', 'F6', 'F7', 'Studio', 'Appartement', 'Espace') NOT NULL,
    localisation VARCHAR(100) NOT NULL,
    prix_nuit DECIMAL(8,2) NOT NULL,
    capacite_max INT NOT NULL,
    nombre_chambres INT NOT NULL,
    nombre_salles_bain INT NOT NULL,
    description TEXT,
    equipements JSON,
    caracteristiques TEXT,
    statut ENUM('disponible', 'indisponible', 'maintenance') DEFAULT 'disponible',
    featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_slug (slug),
    INDEX idx_statut (statut),
    INDEX idx_type (type)
);

-- 2. TABLE IMAGES VILLAS
CREATE TABLE villa_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    villa_id INT NOT NULL,
    nom_fichier VARCHAR(255) NOT NULL,
    nom_original VARCHAR(255) NOT NULL,
    alt_text VARCHAR(255),
    ordre_affichage INT DEFAULT 0,
    image_principale BOOLEAN DEFAULT FALSE,
    taille_fichier INT DEFAULT 0,
    dimensions VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (villa_id) REFERENCES villas(id) ON DELETE CASCADE,
    INDEX idx_villa_id (villa_id),
    INDEX idx_principale (image_principale)
);

-- 3. TABLE ADMIN USERS
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100),
    role ENUM('admin', 'manager') DEFAULT 'manager',
    actif BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_email (email),
    INDEX idx_role (role)
);

-- 4. INSERTION UTILISATEUR ADMIN PAR DEFAUT
-- Mot de passe : "admin123" (à changer immédiatement)
INSERT INTO admin_users (email, password_hash, nom, prenom, role) 
VALUES ('admin@khanelconcept.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Admin', 'KhanelConcept', 'admin');

-- 5. INSERTION DES VILLAS DE BASE (21 villas existantes)
INSERT INTO villas (nom, slug, type, localisation, prix_nuit, capacite_max, nombre_chambres, nombre_salles_bain, description, caracteristiques) VALUES

('Villa F3 sur Petit Macabou', 'villa-f3-petit-macabou', 'F3', 'Petit Macabou, Vauclin', 850.00, 6, 3, 2, 'Villa moderne avec terrasses panoramiques et vue exceptionnelle', 'Piscine, Vue mer, Terrasses modernes, Vue panoramique'),

('Villa F5 sur Ste Anne', 'villa-f5-ste-anne', 'F5', 'Sainte-Anne', 1350.00, 10, 5, 3, 'Grande villa familiale avec piscine et jardin tropical', 'Piscine, Villa rose, Terrasse couverte, Chambres enfants'),

('Villa F6 sur Petit Macabou', 'villa-f6-petit-macabou', 'F6', 'Petit Macabou, Vauclin', 2000.00, 12, 6, 4, 'Villa de luxe avec vue aérienne et équipements premium', 'Villa luxe, Vue aérienne, Terrasses panoramiques, Mezzanine'),

('Studio Cocooning Lamentin', 'studio-cocooning-lamentin', 'Studio', 'Lamentin', 400.00, 2, 1, 1, 'Studio intimiste avec jacuzzi et décoration moderne', 'Studio, Jacuzzi, Terrasse, Cuisine moderne'),

('Espace Piscine Journée Bungalow', 'espace-piscine-journee-bungalow', 'Espace', 'Bungalow', 350.00, 150, 3, 2, 'Espace événementiel avec piscine et bungalow créole', 'Piscine, Événements, Bungalow créole, Studio kitchenette'),

('Villa F3 pour la Baccha', 'villa-f3-baccha', 'F3', 'Petit Macabou', 850.00, 6, 3, 2, 'Villa familiale avec terrasse jardin et piscine', 'Piscine, Terrasse jardin, Cuisine équipée, Chambre moderne'),

('Villa F5 Vauclin Ravine Plate', 'villa-f5-vauclin-ravine-plate', 'F5', 'Vauclin, Ravine Plate', 1800.00, 10, 5, 3, 'Villa avec piscine à débordement et vue panoramique', 'Piscine à débordement, Vue panoramique, Gazebo, Poutres apparentes'),

('Villa F7 Baie des Mulets', 'villa-f7-baie-des-mulets', 'F7', 'Baie des Mulets, Vauclin', 2200.00, 14, 7, 4, 'Grande villa avec véranda bambou et espaces détente', 'Véranda bambou, Salon canapé angle, Chambre principale, Coin détente'),

('Villa F3 sur Le François', 'villa-f3-le-francois', 'F3', 'Le François', 950.00, 6, 3, 2, 'Villa avec terrasse vue mer et salon extérieur', 'Terrasse vue mer, Salon extérieur, Cuisine bleue, Vue aérienne'),

('Villa F6 sur Ste Luce à 1mn de la plage', 'villa-f6-ste-luce-plage', 'F6', 'Sainte-Luce', 2200.00, 12, 6, 4, 'Villa premium proche plage avec vue aérienne piscine', 'Vue aérienne piscine, Salon piscine, Chambre poutres, Salle à manger'),

('Villa F5 La Renée', 'villa-f5-la-renee', 'F5', 'Rivière-Pilote, La Renée', 1500.00, 10, 5, 3, 'Villa avec terrasse bois et ambiance tropicale', 'Terrasse bois palmiers, Salon cuir noir, Cuisine bois clair, Hamacs'),

('Villa F6 au Lamentin', 'villa-f6-lamentin', 'F6', 'Lamentin', 1900.00, 12, 6, 4, 'Villa moderne avec piscine jacuzzi et vue ensemble', 'Piscine jacuzzi, Vue ensemble, Terrasse moderne'),

('Bas Villa F3 sur Le Robert', 'bas-villa-f3-robert', 'F3', 'Le Robert, Pointe Hyacinthe', 750.00, 6, 3, 2, 'Villa avec piscine rectangulaire et terrasse pergola', 'Piscine rectangulaire, Terrasse pergola, Salon TV, Cuisine ouverte'),

('Bas Villa F3 sur Ste Luce', 'bas-villa-f3-ste-luce', 'F3', 'Sainte-Luce', 650.00, 6, 3, 2, 'Villa avec terrasse lounge et équipements modernes', 'Terrasse lounge, Salon TV LED, Chambre climatisée, Coin repas'),

('Villa F3 Trinité Cosmy', 'villa-f3-trinite-cosmy', 'F3', 'La Trinité, Cosmy', 800.00, 6, 3, 2, 'Villa avec piscine chauffée et vue sur collines', 'Piscine chauffée, Vue collines, Cuisine jaune bois, Terrasse couverte'),

('Appartement F3 Trenelle', 'appartement-f3-trenelle', 'Appartement', 'Trenelle', 500.00, 6, 3, 2, 'Appartement pour location avec équipements complets', 'Location annuelle, Salon TV, Cuisine équipée, Espace détente'),

('Villa Fête Journée Ducos', 'villa-fete-ducos', 'Espace', 'Ducos', 400.00, 50, 2, 2, 'Espace événementiel avec piscine et aires de jeux', 'Piscine jouets, Terrasse salon, Bar gazebo, Salon rotin'),

('Villa Fête Journée Fort-de-France', 'villa-fete-fort-de-france', 'Espace', 'Fort-de-France', 600.00, 80, 3, 3, 'Espace premium pour événements avec décor exotique', 'Piscine Buddha, Terrasse colonnes, Véranda coloniale, Allée palmiers'),

('Villa Fête Journée Rivière-Salée', 'villa-fete-riviere-salee', 'Espace', 'Rivière-Salée', 450.00, 60, 2, 2, 'Espace couvert pour événements toute saison', 'Piscine tente couverte, Événements'),

('Villa Fête Journée Rivière-Pilote', 'villa-fete-riviere-pilote', 'Espace', 'Rivière-Pilote', 500.00, 70, 3, 2, 'Villa créole pour événements avec piscine tropicale', 'Salle à manger, Piscine tropicale, Villa créole, Terrasse pierre'),

('Villa Fête Journée Sainte-Luce', 'villa-fete-sainte-luce', 'Espace', 'Sainte-Luce', 550.00, 100, 4, 3, 'Grande villa contemporaine pour événements d envergure', 'Tentes amenagement, Villa contemporaine, Décoration anniversaire, Toilettes extérieures');

-- 6. VERIFICATION ET STATISTIQUES
SELECT 'TABLES CREEES AVEC SUCCES' as status;
SELECT COUNT(*) as total_villas FROM villas;
SELECT COUNT(*) as total_admins FROM admin_users;
SELECT 'INSTALLATION TERMINEE' as final_status;