// Frontend-Backend Synchronization System
class SyncManager {
    constructor(app) {
        this.app = app;
        this.syncInProgress = false;
    }

    // Main synchronization method
    async syncWithMainSite() {
        if (this.syncInProgress) {
            console.log('Sync already in progress...');
            return;
        }

        this.syncInProgress = true;
        console.log('🔄 Starting sync with main site...');

        try {
            // 1. Update localStorage for main site
            await this.updateMainSiteData();
            
            // 2. Generate JavaScript data for main site files
            await this.generateVillaDetailsData();
            
            // 3. Update index.html data
            await this.generateIndexData();
            
            // 4. Show success notification
            this.app.showToast('✅ Synchronisation avec le site principal réussie', 'success');
            
            console.log('✅ Sync completed successfully');
            
        } catch (error) {
            console.error('❌ Sync error:', error);
            this.app.showToast('❌ Erreur de synchronisation: ' + error.message, 'error');
        } finally {
            this.syncInProgress = false;
        }
    }

    // Update data for main site access
    updateMainSiteData() {
        return new Promise((resolve) => {
            const mainSiteVillas = this.app.villas
                .filter(villa => villa.status === 'active')
                .map(villa => ({
                    id: villa.id,
                    name: villa.name,
                    location: villa.location,
                    price: villa.price + '€ /nuit',
                    guests: villa.capacity + ' personnes',
                    image: villa.photos && villa.photos[0] ? villa.photos[0] : './images/placeholder.jpg',
                    gallery: villa.photos || [],
                    description: villa.description,
                    amenities: this.formatAmenitiesForMainSite(villa.amenities || [])
                }));

            // Store data that main site can access
            localStorage.setItem('main_site_sync_data', JSON.stringify({
                villas: mainSiteVillas,
                lastSync: new Date().toISOString(),
                adminVersion: '1.0'
            }));

            console.log(`📊 Updated main site data: ${mainSiteVillas.length} active villas`);
            resolve();
        });
    }

    // Generate villa-details.html compatible data
    generateVillaDetailsData() {
        return new Promise((resolve) => {
            const villaDetailsData = {};
            
            this.app.villas
                .filter(villa => villa.status === 'active')
                .forEach(villa => {
                    villaDetailsData[villa.id] = {
                        name: villa.name,
                        location: "📍 " + villa.location,
                        price: villa.price + "€ /nuit",
                        guests: "👥 " + villa.capacity + " personnes",
                        image: villa.photos && villa.photos[0] ? villa.photos[0] : "./images/placeholder.jpg",
                        gallery: villa.photos || [],
                        description: villa.description,
                        amenities: this.formatAmenitiesForVillaDetails(villa.amenities || [])
                    };
                });

            // Store in special key for villa-details.html
            localStorage.setItem('villa_details_data', JSON.stringify(villaDetailsData));
            
            console.log(`🏠 Generated villa-details data for ${Object.keys(villaDetailsData).length} villas`);
            resolve();
        });
    }

    // Generate index.html compatible data  
    generateIndexData() {
        return new Promise((resolve) => {
            const indexData = this.app.villas
                .filter(villa => villa.status === 'active')
                .map(villa => ({
                    id: villa.id,
                    name: villa.name,
                    price: villa.price,
                    guests: villa.capacity + " personnes",
                    guestsDetail: `${villa.capacity} personnes + invités`,
                    features: (villa.amenities || []).join(', '),
                    category: villa.capacity > 15 ? 'fete' : 'sejour',
                    image: villa.photos && villa.photos[0] ? villa.photos[0] : "./images/placeholder.jpg",
                    gallery: villa.photos || [],
                    fallbackIcon: this.getVillaIcon(villa),
                    location: villa.location
                }));

            // Store for index.html
            localStorage.setItem('index_villas_data', JSON.stringify(indexData));
            
            console.log(`📝 Generated index data for ${indexData.length} villas`);
            resolve();
        });
    }

    // Format amenities for main site
    formatAmenitiesForMainSite(amenities) {
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

    // Format amenities for villa-details.html
    formatAmenitiesForVillaDetails(amenities) {
        return this.formatAmenitiesForMainSite(amenities);
    }

    // Get villa icon based on amenities
    getVillaIcon(villa) {
        if (villa.amenities) {
            if (villa.amenities.includes('piscine')) return '🏊';
            if (villa.amenities.includes('vue-mer')) return '🌊';
            if (villa.amenities.includes('jacuzzi')) return '🛁';
            if (villa.amenities.includes('plage')) return '🏖️';
        }
        return '🏠';
    }

    // Utility function
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    // Real-time sync trigger (called when villa data changes)
    triggerRealTimeSync() {
        // Debounce to avoid too many sync calls
        clearTimeout(this.syncTimeout);
        this.syncTimeout = setTimeout(() => {
            this.syncWithMainSite();
        }, 1000);
    }

    // Export updated data for main site files
    exportMainSiteUpdate() {
        const syncData = localStorage.getItem('main_site_sync_data');
        if (!syncData) {
            this.app.showToast('❌ Aucune donnée à exporter', 'error');
            return;
        }

        // Create downloadable update
        const updateData = {
            villaDetailsData: JSON.parse(localStorage.getItem('villa_details_data') || '{}'),
            indexVillasData: JSON.parse(localStorage.getItem('index_villas_data') || '[]'),
            syncInfo: JSON.parse(syncData),
            updateInstructions: {
                villaDetails: 'Replace the villas object in villa-details.html with villaDetailsData',
                indexPage: 'Replace the villasData array in index.html with indexVillasData',
                timestamp: new Date().toISOString()
            }
        };

        // Download update file
        const blob = new Blob([JSON.stringify(updateData, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `khanelconcept-site-update-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.app.showToast('📥 Mise à jour du site principal exportée', 'success');
    }

    // Live preview integration
    showLivePreview(villaId) {
        // Open villa-details.html with updated data
        const previewUrl = `../villa-details.html?id=${villaId}&preview=admin`;
        const previewWindow = window.open(previewUrl, '_blank');
        
        // Inject updated data into preview
        if (previewWindow) {
            previewWindow.addEventListener('load', () => {
                const villaData = JSON.parse(localStorage.getItem('villa_details_data') || '{}');
                previewWindow.postMessage({
                    type: 'ADMIN_PREVIEW_DATA',
                    data: villaData
                }, '*');
            });
        }
    }
}

// Auto-sync when data changes
if (typeof window !== 'undefined' && window.app) {
    window.app.syncManager = new SyncManager(window.app);
    
    // Override save data to trigger sync
    const originalSaveData = window.app.saveData;
    window.app.saveData = function() {
        originalSaveData.call(this);
        if (this.syncManager) {
            this.syncManager.triggerRealTimeSync();
        }
    };
}

// Global functions for UI
function exportSiteUpdate() {
    if (window.app && window.app.syncManager) {
        window.app.syncManager.exportMainSiteUpdate();
    }
}

function previewVilla(villaId) {
    if (window.app && window.app.syncManager) {
        window.app.syncManager.showLivePreview(villaId);
    }
}