
// PROTECTION IMAGES/VIDÉOS - NE PAS SUPPRIMER
function protectMediaElements() {
    const mediaElements = document.querySelectorAll('img, video');
    mediaElements.forEach(element => {
        element.setAttribute('data-protected', 'true');
    });
}

// Protéger avant toute modification DOM
if (typeof MutationObserver !== 'undefined') {
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                // Vérifier que les éléments média ne sont pas supprimés
                mutation.removedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && (node.tagName === 'IMG' || node.tagName === 'VIDEO')) {
                        console.warn('⚠️ Tentative de suppression d\'élément média détectée:', node);
                    }
                });
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}


/**
 * SERVEUR BACKEND ADMIN PROPRIÉTAIRES
 * ===================================
 * 
 * Backend Node.js/Express pour l'interface admin propriétaires
 * Inclut : authentification par codes, gestion villas, calendrier, SQLite
 */

const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const path = require('path');
const fs = require('fs').promises;
const { v4: uuidv4 } = require('uuid');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;
const JWT_SECRET = process.env.JWT_SECRET || 'khanel_admin_secret_key_2024';
const DB_PATH = path.join(__dirname, 'admin_proprietaires.db');

// =====================================
// MIDDLEWARE
// =====================================

app.use(helmet({
    contentSecurityPolicy: false // Désactivé pour développement
}));

app.use(cors({
    origin: ['http://localhost:8080', 'http://127.0.0.1:8080', 'http://localhost:3000', 'http://127.0.0.1:3000'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Rate limiting
const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // limite de 100 requêtes par IP
    message: { error: 'Trop de requêtes, réessayez plus tard' }
});
app.use('/api/', limiter);

// Rate limiting spécial pour auth
const authLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    max: 5, // 5 tentatives de connexion par IP
    message: { error: 'Trop de tentatives de connexion' }
});
app.use('/api/auth/', authLimiter);

// =====================================
// BASE DE DONNÉES
// =====================================

class Database {
    constructor() {
        this.db = null;
    }

    async init() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(DB_PATH, (err) => {
                if (err) {
                    console.error('Erreur connexion SQLite:', err);
                    reject(err);
                } else {
                    console.log('✅ Connexion SQLite établie');
                    this.createTables().then(resolve).catch(reject);
                }
            });
        });
    }

    async createTables() {
        const queries = [
            // Table des villas
            `CREATE TABLE IF NOT EXISTS villas (
                id TEXT PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                capacity INTEGER,
                bedrooms INTEGER,
                bathrooms INTEGER,
                surface INTEGER,
                default_price REAL,
                description TEXT,
                image TEXT,
                owner_email TEXT,
                owner_password TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )`,
            
            // Table des codes d'accès
            `CREATE TABLE IF NOT EXISTS access_codes (
                id TEXT PRIMARY KEY,
                code TEXT UNIQUE NOT NULL,
                villa_id TEXT NOT NULL,
                expires_at DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                used_at DATETIME,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (villa_id) REFERENCES villas (id)
            )`,
            
            // Table des disponibilités/calendrier
            `CREATE TABLE IF NOT EXISTS availabilities (
                id TEXT PRIMARY KEY,
                villa_id TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('available', 'booked', 'blocked')),
                price_per_night REAL,
                reason TEXT,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (villa_id) REFERENCES villas (id)
            )`,
            
            // Table des réservations (simulées)
            `CREATE TABLE IF NOT EXISTS reservations (
                id TEXT PRIMARY KEY,
                villa_id TEXT NOT NULL,
                client_name TEXT,
                client_email TEXT,
                client_phone TEXT,
                checkin_date DATE NOT NULL,
                checkout_date DATE NOT NULL,
                total_amount REAL,
                status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (villa_id) REFERENCES villas (id)
            )`
        ];

        for (const query of queries) {
            await this.run(query);
        }
        
        console.log('✅ Tables créées/vérifiées');
    }

    run(query, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(query, params, function(err) {
                if (err) reject(err);
                else resolve({ id: this.lastID, changes: this.changes });
            });
        });
    }

    get(query, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(query, params, (err, row) => {
                if (err) reject(err);
                else resolve(row);
            });
        });
    }

    all(query, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(query, params, (err, rows) => {
                if (err) reject(err);
                else resolve(rows);
            });
        });
    }
}

const database = new Database();

// =====================================
// UTILITAIRES
// =====================================

// Génération de codes villa basés sur le nom
function generateVillaCode(villaName) {
    // Extraire les initiales et ajouter des chiffres aléatoires
    const words = villaName.split(' ').filter(word => word.length > 2);
    let code = '';
    
    // Prendre 2-3 lettres des mots principaux
    words.slice(0, 2).forEach(word => {
        code += word.substring(0, 2).toUpperCase();
    });
    
    // Ajouter des chiffres pour compléter à 6 caractères
    while (code.length < 6) {
        code += Math.floor(Math.random() * 10);
    }
    
    return code.substring(0, 6);
}

// Middleware d'authentification
const authenticateToken = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Token d\'accès requis' });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({ error: 'Token invalide' });
        }
        req.user = user;
        next();
    });
};

// =====================================
// ROUTES D'AUTHENTIFICATION
// =====================================

// Validation d'un code d'accès
app.post('/api/auth/validate-code', async (req, res) => {
    try {
        const { code } = req.body;
        
        if (!code || !/^[A-Z0-9]{6}$/.test(code)) {
            return res.status(400).json({ 
                success: false, 
                message: 'Code invalide. Format attendu: 6 caractères alphanumériques' 
            });
        }

        // Vérifier le code et récupérer la villa
        const accessCode = await database.get(`
            SELECT ac.*, v.*
            FROM access_codes ac
            JOIN villas v ON ac.villa_id = v.id
            WHERE ac.code = ? AND ac.is_active = 1 AND ac.expires_at > datetime('now')
        `, [code]);

        if (!accessCode) {
            return res.status(401).json({ 
                success: false, 
                message: 'Code invalide ou expiré' 
            });
        }

        // Marquer le code comme utilisé
        await database.run(`
            UPDATE access_codes 
            SET used_at = datetime('now')
            WHERE code = ?
        `, [code]);

        // Générer JWT
        const token = jwt.sign(
            { 
                villaId: accessCode.villa_id,
                villaCode: accessCode.code,
                access: 'proprietaire'
            },
            JWT_SECRET,
            { expiresIn: '24h' }
        );

        const villa = {
            id: accessCode.villa_id,
            code: accessCode.code,
            name: accessCode.name,
            location: accessCode.location,
            capacity: accessCode.capacity,
            default_price: accessCode.default_price,
            description: accessCode.description,
            image: accessCode.image
        };

        res.json({
            success: true,
            token,
            villa,
            message: 'Connexion réussie'
        });

    } catch (error) {
        console.error('Erreur validation code:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Erreur serveur' 
        });
    }
});

// Connexion email/password (fallback)
app.post('/api/auth/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({ 
                success: false, 
                message: 'Email et mot de passe requis' 
            });
        }

        const villa = await database.get(`
            SELECT * FROM villas 
            WHERE owner_email = ? AND is_active = 1
        `, [email]);

        if (!villa) {
            return res.status(401).json({ 
                success: false, 
                message: 'Identifiants invalides' 
            });
        }

        // Vérifier le mot de passe
        const isValidPassword = villa.owner_password ? 
            await bcrypt.compare(password, villa.owner_password) : 
            false;

        if (!isValidPassword) {
            return res.status(401).json({ 
                success: false, 
                message: 'Identifiants invalides' 
            });
        }

        // Générer JWT
        const token = jwt.sign(
            { 
                villaId: villa.id,
                villaCode: villa.code,
                access: 'proprietaire'
            },
            JWT_SECRET,
            { expiresIn: '24h' }
        );

        const villaData = {
            id: villa.id,
            code: villa.code,
            name: villa.name,
            location: villa.location,
            capacity: villa.capacity,
            default_price: villa.default_price,
            description: villa.description,
            image: villa.image
        };

        res.json({
            success: true,
            token,
            villa: villaData,
            message: 'Connexion réussie'
        });

    } catch (error) {
        console.error('Erreur connexion email:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Erreur serveur' 
        });
    }
});

// Validation du token
app.get('/api/auth/validate-token', authenticateToken, async (req, res) => {
    try {
        const villa = await database.get(`
            SELECT id, code, name, location, capacity, default_price, description, image
            FROM villas 
            WHERE id = ? AND is_active = 1
        `, [req.user.villaId]);

        if (!villa) {
            return res.status(404).json({ 
                success: false, 
                message: 'Villa non trouvée' 
            });
        }

        res.json({
            success: true,
            villa
        });

    } catch (error) {
        console.error('Erreur validation token:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Erreur serveur' 
        });
    }
});

// =====================================
// ROUTES VILLA
// =====================================

// Statistiques villa
app.get('/api/villa/stats', authenticateToken, async (req, res) => {
    try {
        const villaId = req.user.villaId;
        const currentMonth = new Date().toISOString().slice(0, 7); // YYYY-MM
        
        // Compter les disponibilités par type
        const stats = await database.all(`
            SELECT 
                type,
                COUNT(*) as count,
                SUM(CASE WHEN type = 'booked' THEN COALESCE(price_per_night, 0) ELSE 0 END) as revenue
            FROM availabilities 
            WHERE villa_id = ? AND strftime('%Y-%m', start_date) = ?
            GROUP BY type
        `, [villaId, currentMonth]);

        const result = {
            availableDays: 0,
            bookedDays: 0,
            blockedDays: 0,
            totalRevenue: 0
        };

        stats.forEach(stat => {
            switch(stat.type) {
                case 'available':
                    result.availableDays = stat.count;
                    break;
                case 'booked':
                    result.bookedDays = stat.count;
                    result.totalRevenue = Math.round(stat.revenue || 0);
                    break;
                case 'blocked':
                    result.blockedDays = stat.count;
                    break;
            }
        });

        res.json(result);

    } catch (error) {
        console.error('Erreur stats villa:', error);
        res.status(500).json({ error: 'Erreur serveur' });
    }
});

// Calendrier villa
app.get('/api/villa/calendar', authenticateToken, async (req, res) => {
    try {
        const { start, end } = req.query;
        const villaId = req.user.villaId;

        const availabilities = await database.all(`
            SELECT id, start_date, end_date, type, price_per_night, reason, notes
            FROM availabilities 
            WHERE villa_id = ? 
            AND ((start_date BETWEEN ? AND ?) OR (end_date BETWEEN ? AND ?))
            ORDER BY start_date
        `, [villaId, start, end, start, end]);

        // Format pour FullCalendar
        const events = availabilities.map(avail => ({
            id: avail.id,
            title: getEventTitle(avail.type, avail.price_per_night),
            start: avail.start_date,
            end: avail.end_date,
            className: avail.type,
            backgroundColor: getEventColor(avail.type),
            borderColor: getEventColor(avail.type),
            extendedProps: {
                type: avail.type,
                price: avail.price_per_night,
                reason: avail.reason,
                notes: avail.notes,
                description: avail.notes || avail.reason || ''
            }
        }));

        res.json(events);

    } catch (error) {
        console.error('Erreur calendrier villa:', error);
        res.status(500).json({ error: 'Erreur serveur' });
    }
});

// Réservations villa
app.get('/api/villa/reservations', authenticateToken, async (req, res) => {
    try {
        const villaId = req.user.villaId;
        
        const reservations = await database.all(`
            SELECT *
            FROM reservations 
            WHERE villa_id = ?
            ORDER BY created_at DESC
            LIMIT 10
        `, [villaId]);

        res.json(reservations);

    } catch (error) {
        console.error('Erreur réservations villa:', error);
        res.status(500).json({ error: 'Erreur serveur' });
    }
});

// Ajouter disponibilité
app.post('/api/villa/availability', authenticateToken, async (req, res) => {
    try {
        const { start_date, end_date, type, price_per_night, reason, notes } = req.body;
        const villaId = req.user.villaId;

        if (!start_date || !end_date || !type) {
            return res.status(400).json({ 
                success: false, 
                message: 'Dates et type requis' 
            });
        }

        // Vérifier les conflits
        const conflict = await database.get(`
            SELECT id FROM availabilities
            WHERE villa_id = ? 
            AND ((start_date BETWEEN ? AND ?) OR (end_date BETWEEN ? AND ?))
            AND type IN ('booked', 'blocked', 'available')
        `, [villaId, start_date, end_date, start_date, end_date]);

        if (conflict) {
            return res.status(409).json({ 
                success: false, 
                message: 'Conflit de dates détecté' 
            });
        }

        const id = uuidv4();
        await database.run(`
            INSERT INTO availabilities (id, villa_id, start_date, end_date, type, price_per_night, reason, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `, [id, villaId, start_date, end_date, type, price_per_night, reason, notes]);

        res.json({
            success: true,
            message: 'Disponibilité ajoutée avec succès',
            id
        });

    } catch (error) {
        console.error('Erreur ajout disponibilité:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Erreur serveur' 
        });
    }
});

// Supprimer disponibilité
app.delete('/api/villa/availability/:id', authenticateToken, async (req, res) => {
    try {
        const { id } = req.params;
        const villaId = req.user.villaId;

        const result = await database.run(`
            DELETE FROM availabilities
            WHERE id = ? AND villa_id = ?
        `, [id, villaId]);

        if (result.changes === 0) {
            return res.status(404).json({ 
                success: false, 
                message: 'Disponibilité non trouvée' 
            });
        }

        res.json({
            success: true,
            message: 'Disponibilité supprimée avec succès'
        });

    } catch (error) {
        console.error('Erreur suppression disponibilité:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Erreur serveur' 
        });
    }
});

// Export calendrier CSV
app.get('/api/villa/export-calendar', authenticateToken, async (req, res) => {
    try {
        const villaId = req.user.villaId;
        
        const availabilities = await database.all(`
            SELECT start_date, end_date, type, price_per_night, reason, notes
            FROM availabilities 
            WHERE villa_id = ?
            ORDER BY start_date
        `, [villaId]);

        // Générer CSV
        let csv = 'Date Début,Date Fin,Type,Prix/Nuit,Raison,Notes\n';
        
        availabilities.forEach(avail => {
            csv += `${avail.start_date},${avail.end_date},${avail.type},${avail.price_per_night || ''},${avail.reason || ''},${avail.notes || ''}\n`;
        });

        res.setHeader('Content-Type', 'text/csv');
        res.setHeader('Content-Disposition', 'attachment; filename=calendrier.csv');
        res.send(csv);

    } catch (error) {
        console.error('Erreur export calendrier:', error);
        res.status(500).json({ error: 'Erreur serveur' });
    }
});

// =====================================
// FONCTIONS UTILITAIRES
// =====================================

function getEventTitle(type, price) {
    switch(type) {
        case 'available':
            return price ? `Disponible ${price}€` : 'Disponible';
        case 'booked':
            return price ? `Réservé ${price}€` : 'Réservé';
        case 'blocked':
            return 'Bloqué';
        default:
            return type;
    }
}

function getEventColor(type) {
    switch(type) {
        case 'available': return '#10b981'; // Vert
        case 'booked': return '#ef4444'; // Rouge
        case 'blocked': return '#6b7280'; // Gris
        default: return '#3b82f6'; // Bleu
    }
}

// Route de test
app.get('/api/health', (req, res) => {
    res.json({ 
        status: 'OK', 
        message: 'API Admin Propriétaires opérationnelle',
        timestamp: new Date().toISOString()
    });
});

// =====================================
// DÉMARRAGE SERVEUR
// =====================================

async function startServer() {
    try {
        // Initialiser la base de données
        await database.init();
        
        // Démarrer le serveur
        app.listen(PORT, () => {
            console.log('🚀 ==========================================');
            console.log(`🏠 SERVEUR ADMIN PROPRIÉTAIRES DÉMARRÉ`);
            console.log(`📡 Port: ${PORT}`);
            console.log(`🗄️  Base de données: ${DB_PATH}`);
            console.log(`🔑 JWT Secret: ${JWT_SECRET.substring(0, 10)}...`);
            console.log('🚀 ==========================================');
            console.log(`✅ API disponible sur: http://localhost:${PORT}/api/health`);
        });
        
    } catch (error) {
        console.error('❌ Erreur démarrage serveur:', error);
        process.exit(1);
    }
}

// Gestion des arrêts propres
process.on('SIGINT', () => {
    console.log('\n🛑 Arrêt du serveur...');
    if (database.db) {
        database.db.close();
    }
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Arrêt du serveur...');
    if (database.db) {
        database.db.close();
    }
    process.exit(0);
});

// Démarrer
startServer();