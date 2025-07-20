// Data Export/Import Manager

class DataExportManager {
    constructor(app) {
        this.app = app;
    }

    // Export all data
    exportAllData() {
        const data = {
            villas: this.app.villas,
            settings: this.app.settings,
            images: JSON.parse(localStorage.getItem('admin_images')) || [],
            reservations: JSON.parse(localStorage.getItem('admin_reservations')) || [],
            metadata: {
                exportDate: new Date().toISOString(),
                version: '1.0',
                totalVillas: this.app.villas.length,
                totalImages: (JSON.parse(localStorage.getItem('admin_images')) || []).length
            }
        };

        this.downloadJSON(data, `khanelconcept-full-backup-${this.getDateString()}.json`);
        this.app.showToast('Sauvegarde complète exportée avec succès', 'success');
    }

    // Export only villas
    exportVillas() {
        const data = {
            villas: this.app.villas,
            exported: new Date().toISOString(),
            total: this.app.villas.length
        };

        this.downloadJSON(data, `khanelconcept-villas-${this.getDateString()}.json`);
        this.app.showToast('Villas exportées avec succès', 'success');
    }

    // Export settings
    exportSettings() {
        const data = {
            settings: this.app.settings,
            exported: new Date().toISOString()
        };

        this.downloadJSON(data, `khanelconcept-settings-${this.getDateString()}.json`);
        this.app.showToast('Paramètres exportés avec succès', 'success');
    }

    // Import all data
    importAllData() {
        this.selectFile('.json', (file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    if (this.validateFullBackup(data)) {
                        this.showImportConfirmation(data, () => {
                            this.app.villas = data.villas;
                            this.app.settings = data.settings;
                            
                            if (data.images) {
                                localStorage.setItem('admin_images', JSON.stringify(data.images));
                            }
                            if (data.reservations) {
                                localStorage.setItem('admin_reservations', JSON.stringify(data.reservations));
                            }

                            this.app.saveData();
                            this.app.updateDashboard();
                            this.app.loadVillasGrid();
                            this.app.loadSettings();
                            
                            // Reload image gallery if on images section
                            if (window.imageHandler) {
                                window.imageHandler.uploadedImages = data.images || [];
                                window.imageHandler.loadImageGallery();
                            }

                            this.app.showToast('Données importées avec succès', 'success');
                        });
                    } else {
                        this.app.showToast('Format de fichier de sauvegarde invalide', 'error');
                    }
                } catch (error) {
                    this.app.showToast('Erreur lors de la lecture du fichier', 'error');
                    console.error('Import error:', error);
                }
            };
            reader.readAsText(file);
        });
    }

    // Import villas only
    importVillas() {
        this.selectFile('.json', (file) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const data = JSON.parse(e.target.result);
                    
                    if (data.villas && Array.isArray(data.villas)) {
                        const importType = confirm(
                            'Comment importer les villas ?\n' +
                            'OK = Remplacer toutes les villas existantes\n' +
                            'Annuler = Ajouter aux villas existantes'
                        );

                        if (importType) {
                            // Replace all
                            this.app.villas = data.villas;
                        } else {
                            // Merge - Add new villas
                            let addedCount = 0;
                            data.villas.forEach(importVilla => {
                                // Check if villa exists by name
                                const exists = this.app.villas.find(v => 
                                    v.name.toLowerCase() === importVilla.name.toLowerCase()
                                );
                                
                                if (!exists) {
                                    // Generate new ID
                                    const maxId = this.app.villas.reduce((max, v) => Math.max(max, v.id), 0);
                                    importVilla.id = maxId + 1;
                                    importVilla.created = new Date().toISOString();
                                    importVilla.updated = new Date().toISOString();
                                    
                                    this.app.villas.push(importVilla);
                                    addedCount++;
                                }
                            });

                            this.app.showToast(`${addedCount} nouvelles villas ajoutées`, 'success');
                        }

                        this.app.saveData();
                        this.app.updateDashboard();
                        this.app.loadVillasGrid();
                        
                        this.app.showToast(
                            `${data.villas.length} villas importées avec succès`, 
                            'success'
                        );
                    } else {
                        this.app.showToast('Format de fichier villas invalide', 'error');
                    }
                } catch (error) {
                    this.app.showToast('Erreur lors de la lecture du fichier', 'error');
                    console.error('Import error:', error);
                }
            };
            reader.readAsText(file);
        });
    }

    // Export to different formats
    exportToCSV() {
        if (this.app.villas.length === 0) {
            this.app.showToast('Aucune villa à exporter', 'error');
            return;
        }

        const headers = [
            'ID', 'Nom', 'Prix', 'Capacité', 'Chambres', 'Salle de bains', 
            'Localisation', 'Description', 'Équipements', 'Statut', 'Créé', 'Modifié'
        ];

        const rows = this.app.villas.map(villa => [
            villa.id,
            villa.name,
            villa.price,
            villa.capacity,
            villa.bedrooms || 0,
            villa.bathrooms || 0,
            villa.location,
            `"${villa.description.replace(/"/g, '""')}"`, // Escape quotes
            `"${(villa.amenities || []).join(', ')}"`,
            villa.status,
            villa.created || '',
            villa.updated || ''
        ]);

        const csvContent = [headers, ...rows]
            .map(row => row.join(','))
            .join('\n');

        this.downloadText(csvContent, `khanelconcept-villas-${this.getDateString()}.csv`, 'text/csv');
        this.app.showToast('Villas exportées en CSV avec succès', 'success');
    }

    // Generate website data for integration
    generateWebsiteData() {
        const websiteData = this.app.villas
            .filter(villa => villa.status === 'active')
            .map(villa => ({
                id: villa.id,
                name: villa.name,
                location: villa.location,
                price: villa.price,
                guests: villa.capacity,
                guestsDetail: `${villa.capacity} personnes`,
                features: (villa.amenities || []).join(', '),
                category: 'sejour', // Default category
                image: villa.photos && villa.photos[0] ? villa.photos[0] : './images/placeholder.jpg',
                gallery: villa.photos || [],
                fallbackIcon: this.getVillaIcon(villa),
                description: villa.description,
                amenities: this.formatAmenitiesForWebsite(villa.amenities || [])
            }));

        const jsContent = `// Generated villa data - ${new Date().toISOString()}
const villasData = ${JSON.stringify(websiteData, null, 2)};

// Export for use in main website
if (typeof module !== 'undefined' && module.exports) {
    module.exports = villasData;
}`;

        this.downloadText(
            jsContent, 
            `khanelconcept-website-data-${this.getDateString()}.js`, 
            'text/javascript'
        );
        
        this.app.showToast('Données website générées avec succès', 'success');
    }

    // Helper methods
    validateFullBackup(data) {
        return data && 
               data.villas && Array.isArray(data.villas) &&
               data.settings && typeof data.settings === 'object';
    }

    showImportConfirmation(data, callback) {
        const stats = {
            villas: data.villas ? data.villas.length : 0,
            images: data.images ? data.images.length : 0,
            reservations: data.reservations ? data.reservations.length : 0
        };

        const message = `Importer la sauvegarde ?\n\n` +
                       `• ${stats.villas} villas\n` +
                       `• ${stats.images} images\n` +
                       `• ${stats.reservations} réservations\n\n` +
                       `Cette action remplacera toutes les données actuelles.`;

        if (confirm(message)) {
            callback();
        }
    }

    selectFile(accept, callback) {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = accept;
        input.onchange = (event) => {
            const file = event.target.files[0];
            if (file) {
                callback(file);
            }
        };
        input.click();
    }

    downloadJSON(data, filename) {
        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
        this.downloadBlob(blob, filename);
    }

    downloadText(content, filename, mimeType = 'text/plain') {
        const blob = new Blob([content], {type: mimeType});
        this.downloadBlob(blob, filename);
    }

    downloadBlob(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    getDateString() {
        return new Date().toISOString().split('T')[0];
    }

    getVillaIcon(villa) {
        // Generate appropriate icon based on villa amenities/type
        if (villa.amenities) {
            if (villa.amenities.includes('piscine')) return '🏊';
            if (villa.amenities.includes('vue-mer')) return '🌊';
            if (villa.amenities.includes('jacuzzi')) return '🛁';
            if (villa.amenities.includes('plage')) return '🏖️';
        }
        return '🏠'; // Default icon
    }

    formatAmenitiesForWebsite(amenities) {
        const iconMap = {
            'piscine': '🏊',
            'wifi': '📶',
            'climatisation': '❄️',
            'vue-mer': '🌊',
            'parking': '🚗',
            'cuisine': '🍳',
            'terrasse': '🏖️',
            'barbecue': '🔥',
            'jacuzzi': '🛁',
            'plage': '🏖️',
            'jardin': '🌳',
            'tv': '📺',
            'sauna': '🧖‍♀️'
        };

        return amenities.map(amenity => ({
            icon: iconMap[amenity] || '✨',
            name: this.capitalizeFirst(amenity.replace('-', ' '))
        }));
    }

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    // Backup scheduling (for future implementation)
    scheduleAutoBackup() {
        // This would set up automatic backups
        const lastBackup = localStorage.getItem('admin_last_backup');
        const now = new Date().getTime();
        const dayInMs = 24 * 60 * 60 * 1000;

        if (!lastBackup || (now - parseInt(lastBackup)) > dayInMs) {
            // Perform auto backup
            this.exportAllData();
            localStorage.setItem('admin_last_backup', now.toString());
        }
    }

    // Migration helpers for future API integration
    generateAPIEndpoints() {
        const endpoints = {
            villas: {
                list: 'GET /api/villas',
                create: 'POST /api/villas',
                update: 'PUT /api/villas/:id',
                delete: 'DELETE /api/villas/:id',
                upload_image: 'POST /api/villas/:id/images'
            },
            reservations: {
                list: 'GET /api/reservations',
                create: 'POST /api/reservations',
                update: 'PUT /api/reservations/:id',
                delete: 'DELETE /api/reservations/:id'
            },
            settings: {
                get: 'GET /api/settings',
                update: 'PUT /api/settings'
            }
        };

        const content = `// KhanelConcept API Endpoints Structure
// Generated: ${new Date().toISOString()}

const API_ENDPOINTS = ${JSON.stringify(endpoints, null, 2)};

// Base configuration
const API_CONFIG = {
    baseURL: 'https://your-api-domain.com',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN_HERE'
    }
};

module.exports = { API_ENDPOINTS, API_CONFIG };`;

        this.downloadText(
            content,
            `khanelconcept-api-config-${this.getDateString()}.js`,
            'text/javascript'
        );

        this.app.showToast('Configuration API générée avec succès', 'success');
    }
}

// Global export functions
function exportData() {
    if (window.app && window.app.exportManager) {
        window.app.exportManager.exportAllData();
    }
}

function importData() {
    if (window.app && window.app.exportManager) {
        window.app.exportManager.importAllData();
    }
}

function resetData() {
    if (confirm('Cette action supprimera toutes les données. Cette action est irréversible. Continuer ?')) {
        if (confirm('Êtes-vous absolument certain ? Toutes les villas et paramètres seront perdus.')) {
            localStorage.clear();
            sessionStorage.clear();
            location.reload();
        }
    }
}