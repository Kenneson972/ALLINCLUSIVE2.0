// Admin Main JavaScript
class AdminApp {
    constructor() {
        this.currentSection = 'dashboard';
        this.villas = [];
        this.settings = {};
        this.charts = {};
        
        this.init();
    }

    init() {
        this.loadData();
        this.setupEventListeners();
        this.checkAuthentication();
        
        // Initialize managers
        this.villaManager = new VillaManager(this);
        this.exportManager = new DataExportManager(this);
        
        // Initialize image handler
        window.imageHandler = new ImageHandler(this);
        
        this.updateDashboard();
    }

    checkAuthentication() {
        const adminAccess = sessionStorage.getItem('admin_access');
        if (adminAccess !== 'true') {
            window.location.href = 'login.html';
            return;
        }
        
        // Display username
        const adminUser = sessionStorage.getItem('admin_user') || 'Admin';
        const usernameElement = document.getElementById('adminUsername');
        if (usernameElement) {
            usernameElement.textContent = adminUser;
        }
    }

    loadData() {
        // Load villas from localStorage
        this.villas = JSON.parse(localStorage.getItem('admin_villas')) || this.getDefaultVillas();
        this.settings = JSON.parse(localStorage.getItem('admin_settings')) || this.getDefaultSettings();
    }

    saveData() {
        localStorage.setItem('admin_villas', JSON.stringify(this.villas));
        localStorage.setItem('admin_settings', JSON.stringify(this.settings));
    }

    getDefaultVillas() {
        // Import existing villas from the main site
        return [
            {
                id: 1,
                name: "Villa F3 Petit Macabou",
                description: "Magnifique villa F3 avec sauna et jacuzzi, parfaite pour un séjour de détente en famille.",
                price: 850,
                capacity: 6,
                bedrooms: 2,
                bathrooms: 2,
                location: "Petit Macabou au Vauclin",
                gps: "14.5428, -60.8357",
                amenities: ["piscine", "wifi", "sauna", "jacuzzi", "terrasse"],
                photos: [
                    "./images/Villa_F3_Petit_Macabou/01_piscine_exterieur.jpg",
                    "./images/Villa_F3_Petit_Macabou/02_terrasse_salon_exterieur.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 2,
                name: "Villa F5 Ste Anne",
                description: "Villa F5 distinctive avec sa façade rose emblématique, située dans le quartier résidentiel des Anglais à Sainte-Anne.",
                price: 1300,
                capacity: 10,
                bedrooms: 3,
                bathrooms: 2,
                location: "Quartier Les Anglais, Ste Anne",
                gps: "14.4298, -60.8824",
                amenities: ["piscine", "wifi", "cuisine", "parking", "terrasse"],
                photos: [
                    "./images/Villa_F5_Ste_Anne/01_piscine_principale.jpg",
                    "./images/Villa_F5_Ste_Anne/03_facade_villa_rose.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            },
            {
                id: 3,
                name: "Studio Cocooning Lamentin",
                description: "Studio cocooning romantique au Morne Pitault au Lamentin, avec vue panoramique sur la baie de Fort-de-France.",
                price: 290,
                capacity: 2,
                bedrooms: 1,
                bathrooms: 1,
                location: "Morne Pitault, Lamentin",
                gps: "14.6097, -61.0242",
                amenities: ["jacuzzi", "wifi", "vue-mer", "cuisine"],
                photos: [
                    "./images/Studio_Cocooning_Lamentin/01_studio_vue_ensemble.jpg"
                ],
                status: "active",
                created: new Date().toISOString(),
                updated: new Date().toISOString()
            }
        ];
    }

    getDefaultSettings() {
        return {
            siteName: "KhanelConcept",
            contactEmail: "contact@khanelconcept.com",
            contactPhone: "+596 696 XX XX XX",
            currency: "EUR",
            language: "fr"
        };
    }

    setupEventListeners() {
        // Sidebar navigation
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.getAttribute('data-section');
                this.showSection(section);
            });
        });

        // Search and filters
        const searchInput = document.getElementById('villaSearch');
        if (searchInput) {
            searchInput.addEventListener('input', () => this.filterVillas());
        }

        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter) {
            statusFilter.addEventListener('change', () => this.filterVillas());
        }

        const priceFilter = document.getElementById('priceFilter');
        if (priceFilter) {
            priceFilter.addEventListener('change', () => this.filterVillas());
        }

        // Settings form
        const settingsForm = document.getElementById('settingsForm');
        if (settingsForm) {
            settingsForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.saveSettings();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
                this.saveData();
                this.showToast('Données sauvegardées', 'success');
            }
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    bootstrap.Modal.getInstance(modal)?.hide();
                });
            }
        });
    }

    showSection(sectionName) {
        // Update active menu item
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Update active section
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${sectionName}-section`).classList.add('active');

        // Update page title
        const titles = {
            'dashboard': 'Dashboard',
            'villas': 'Gestion des Villas',
            'reservations': 'Réservations',
            'images': 'Gestion des Images',
            'settings': 'Paramètres'
        };
        document.getElementById('pageTitle').textContent = titles[sectionName];

        this.currentSection = sectionName;

        // Load section-specific data
        switch (sectionName) {
            case 'dashboard':
                this.updateDashboard();
                break;
            case 'villas':
                this.loadVillasGrid();
                break;
            case 'images':
                this.loadImageGallery();
                break;
            case 'settings':
                this.loadSettings();
                break;
        }
    }

    loadImageGallery() {
        if (window.imageHandler) {
            window.imageHandler.loadImageGallery();
        }
    }

    // Villa management methods
    editVilla(villaId) {
        this.villaManager.editVilla(villaId);
    }

    duplicateVilla(villaId) {
        this.villaManager.duplicateVilla(villaId);
    }

    deleteVilla(villaId) {
        this.villaManager.deleteVilla(villaId);
    }

    showAddVillaModal() {
        this.villaManager.showAddVillaModal();

    updateDashboard() {
        // Update stats
        document.getElementById('totalVillas').textContent = this.villas.length;
        document.getElementById('activeVillas').textContent = 
            this.villas.filter(v => v.status === 'active').length;
        document.getElementById('totalReservations').textContent = '0'; // Placeholder
        
        const avgPrice = this.villas.length > 0 ? 
            Math.round(this.villas.reduce((sum, v) => sum + v.price, 0) / this.villas.length) : 0;
        document.getElementById('averagePrice').textContent = `${avgPrice}€`;

        // Update charts
        this.updateCharts();

        // Update recent activity
        this.updateRecentActivity();
    }

    updateCharts() {
        // Price distribution chart
        const priceCtx = document.getElementById('priceChart');
        if (priceCtx && this.charts.priceChart) {
            this.charts.priceChart.destroy();
        }
        
        const priceRanges = {
            '0-500€': this.villas.filter(v => v.price < 500).length,
            '500-1000€': this.villas.filter(v => v.price >= 500 && v.price < 1000).length,
            '1000-1500€': this.villas.filter(v => v.price >= 1000 && v.price < 1500).length,
            '1500€+': this.villas.filter(v => v.price >= 1500).length
        };

        this.charts.priceChart = new Chart(priceCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(priceRanges),
                datasets: [{
                    label: 'Nombre de villas',
                    data: Object.values(priceRanges),
                    backgroundColor: 'rgba(37, 99, 235, 0.8)',
                    borderColor: 'rgba(37, 99, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });

        // Status chart
        const statusCtx = document.getElementById('statusChart');
        if (statusCtx && this.charts.statusChart) {
            this.charts.statusChart.destroy();
        }

        const statusData = {
            'Actif': this.villas.filter(v => v.status === 'active').length,
            'Inactif': this.villas.filter(v => v.status === 'inactive').length
        };

        this.charts.statusChart = new Chart(statusCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(statusData),
                datasets: [{
                    data: Object.values(statusData),
                    backgroundColor: [
                        'rgba(34, 197, 94, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgba(34, 197, 94, 1)',
                        'rgba(239, 68, 68, 1)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    updateRecentActivity() {
        const activityContainer = document.getElementById('recentActivity');
        const recentVillas = this.villas
            .sort((a, b) => new Date(b.updated) - new Date(a.updated))
            .slice(0, 5);

        if (recentVillas.length === 0) {
            activityContainer.innerHTML = '<p class="text-muted">Aucune activité récente</p>';
            return;
        }

        activityContainer.innerHTML = recentVillas.map(villa => `
            <div class="d-flex align-items-center mb-3">
                <div class="me-3">
                    <i class="fas fa-home text-primary"></i>
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-0">${villa.name}</h6>
                    <small class="text-muted">Modifié ${this.formatDate(villa.updated)}</small>
                </div>
                <span class="badge bg-${villa.status === 'active' ? 'success' : 'danger'}">${villa.status}</span>
            </div>
        `).join('');
    }

    loadVillasGrid() {
        this.renderVillas(this.villas);
    }

    renderVillas(villas) {
        const grid = document.getElementById('villasGrid');
        if (!grid) return;

        if (villas.length === 0) {
            grid.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-home fa-3x text-muted mb-3"></i>
                    <h4>Aucune villa trouvée</h4>
                    <p class="text-muted">Commencez par ajouter votre première villa</p>
                    <button class="btn btn-primary" onclick="app.showAddVillaModal()">
                        <i class="fas fa-plus me-2"></i>Ajouter Villa
                    </button>
                </div>
            `;
            return;
        }

        grid.innerHTML = villas.map(villa => `
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card villa-card">
                    <div class="position-relative">
                        <img src="${villa.photos[0] || 'https://via.placeholder.com/300x200'}" 
                             class="card-img-top" alt="${villa.name}">
                        <span class="villa-status status-${villa.status}">
                            ${villa.status === 'active' ? 'Actif' : 'Inactif'}
                        </span>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${villa.name}</h5>
                        <p class="card-text text-muted small">${villa.location}</p>
                        <p class="card-text">${villa.description.substring(0, 100)}...</p>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <div class="villa-price">${villa.price}€</div>
                            <small class="text-muted">
                                <i class="fas fa-users me-1"></i>${villa.capacity} pers.
                            </small>
                        </div>
                        <div class="btn-group w-100" role="group">
                            <button class="btn btn-outline-primary btn-sm" onclick="app.editVilla(${villa.id})">
                                <i class="fas fa-edit"></i> Éditer
                            </button>
                            <button class="btn btn-outline-success btn-sm" onclick="app.duplicateVilla(${villa.id})">
                                <i class="fas fa-copy"></i> Dupliquer
                            </button>
                            <button class="btn btn-outline-danger btn-sm" onclick="app.deleteVilla(${villa.id})">
                                <i class="fas fa-trash"></i> Supprimer
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    filterVillas() {
        const searchTerm = document.getElementById('villaSearch')?.value.toLowerCase() || '';
        const statusFilter = document.getElementById('statusFilter')?.value || '';
        const priceFilter = document.getElementById('priceFilter')?.value || '';

        let filteredVillas = this.villas.filter(villa => {
            const matchesSearch = villa.name.toLowerCase().includes(searchTerm) ||
                                villa.location.toLowerCase().includes(searchTerm) ||
                                villa.description.toLowerCase().includes(searchTerm);

            const matchesStatus = statusFilter === '' || villa.status === statusFilter;

            let matchesPrice = true;
            if (priceFilter) {
                if (priceFilter === '0-500') {
                    matchesPrice = villa.price >= 0 && villa.price < 500;
                } else if (priceFilter === '500-1000') {
                    matchesPrice = villa.price >= 500 && villa.price < 1000;
                } else if (priceFilter === '1000-1500') {
                    matchesPrice = villa.price >= 1000 && villa.price < 1500;
                } else if (priceFilter === '1500+') {
                    matchesPrice = villa.price >= 1500;
                }
            }

            return matchesSearch && matchesStatus && matchesPrice;
        });

        this.renderVillas(filteredVillas);
    }

    clearFilters() {
        document.getElementById('villaSearch').value = '';
        document.getElementById('statusFilter').value = '';
        document.getElementById('priceFilter').value = '';
        this.renderVillas(this.villas);
    }

    loadSettings() {
        document.getElementById('siteName').value = this.settings.siteName || '';
        document.getElementById('contactEmail').value = this.settings.contactEmail || '';
        document.getElementById('contactPhone').value = this.settings.contactPhone || '';
    }

    saveSettings() {
        this.settings = {
            ...this.settings,
            siteName: document.getElementById('siteName').value,
            contactEmail: document.getElementById('contactEmail').value,
            contactPhone: document.getElementById('contactPhone').value
        };
        
        this.saveData();
        this.showToast('Paramètres sauvegardés avec succès', 'success');
    }

    showToast(message, type = 'success') {
        const toastElement = document.getElementById(`${type}Toast`);
        const messageElement = document.getElementById(`${type}Message`);
        
        messageElement.textContent = message;
        
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) return "aujourd'hui";
        if (diffDays === 1) return "hier";
        if (diffDays < 7) return `il y a ${diffDays} jours`;
        return date.toLocaleDateString('fr-FR');
    }
}

// Global functions
function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('show');
}

function logout() {
    if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
        sessionStorage.removeItem('admin_access');
        window.location.href = 'login.html';
    }
}

function exportData() {
    const data = {
        villas: app.villas,
        settings: app.settings,
        exported: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `khanelconcept-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    app.showToast('Données exportées avec succès', 'success');
}

function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = JSON.parse(e.target.result);
                    if (data.villas && data.settings) {
                        if (confirm('Cette action remplacera toutes les données actuelles. Continuer ?')) {
                            app.villas = data.villas;
                            app.settings = data.settings;
                            app.saveData();
                            app.updateDashboard();
                            app.loadVillasGrid();
                            app.loadSettings();
                            app.showToast('Données importées avec succès', 'success');
                        }
                    } else {
                        app.showToast('Format de fichier invalide', 'error');
                    }
                } catch (error) {
                    app.showToast('Erreur lors de la lecture du fichier', 'error');
                }
            };
            reader.readAsText(file);
        }
    };
    input.click();
}

function resetData() {
    if (confirm('Cette action supprimera toutes les données. Cette action est irréversible. Continuer ?')) {
        if (confirm('Êtes-vous absolument certain ? Toutes les villas et paramètres seront perdus.')) {
            localStorage.removeItem('admin_villas');
            localStorage.removeItem('admin_settings');
            location.reload();
        }
    }
}

// Initialize app when page loads
let app;
document.addEventListener('DOMContentLoaded', function() {
    app = new AdminApp();
});