/**
 * ADMIN PROPRIÉTAIRES - JavaScript Principal
 * ==========================================
 * 
 Gestion complète de l'interface admin pour propriétaires de villas
 * Inclut : authentification par code, calendrier, CRUD villa, synchronisation API
 */

class AdminProprietaires {
    constructor() {
        this.API_BASE = 'http://localhost:3002/api';
        this.currentVilla = null;
        this.calendar = null;
        this.token = localStorage.getItem('villa_token');
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.initializeVideoBackground();
        
        // Vérifier si déjà connecté
        if (this.token) {
            try {
                await this.validateToken();
            } catch (error) {
                this.logout();
            }
        }
    }

    setupEventListeners() {
        // Formulaire de connexion par code
        const codeForm = document.getElementById('codeForm');
        if (codeForm) {
            codeForm.addEventListener('submit', (e) => this.handleCodeLogin(e));
        }

        // Formulaire de connexion email/password
        const emailLoginForm = document.getElementById('emailLoginForm');
        if (emailLoginForm) {
            emailLoginForm.addEventListener('submit', (e) => this.handleEmailLogin(e));
        }

        // Bouton afficher login email
        const showLoginForm = document.getElementById('showLoginForm');
        if (showLoginForm) {
            showLoginForm.addEventListener('click', () => this.toggleEmailLogin());
        }

        // Bouton déconnexion
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }

        // Boutons dashboard
        const addAvailabilityBtn = document.getElementById('addAvailabilityBtn');
        if (addAvailabilityBtn) {
            addAvailabilityBtn.addEventListener('click', () => this.showAvailabilityModal());
        }

        const blockDatesBtn = document.getElementById('blockDatesBtn');
        if (blockDatesBtn) {
            blockDatesBtn.addEventListener('click', () => this.showBlockModal());
        }

        const editVillaBtn = document.getElementById('editVillaBtn');
        if (editVillaBtn) {
            editVillaBtn.addEventListener('click', () => this.editVilla());
        }

        const exportBtn = document.getElementById('exportBtn');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportCalendar());
        }

        // Modals
        this.setupModalListeners();

        // Formulaires modals
        const availabilityForm = document.getElementById('availabilityForm');
        if (availabilityForm) {
            availabilityForm.addEventListener('submit', (e) => this.handleAvailabilitySubmit(e));
        }

        const blockForm = document.getElementById('blockForm');
        if (blockForm) {
            blockForm.addEventListener('submit', (e) => this.handleBlockSubmit(e));
        }

        // Validation en temps réel du code
        const accessCode = document.getElementById('accessCode');
        if (accessCode) {
            accessCode.addEventListener('input', (e) => this.validateCodeFormat(e));
        }
    }

    setupModalListeners() {
        // Fermeture des modals
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                this.closeModal(e.target.closest('.fixed'));
            });
        });

        // Fermeture en cliquant sur l'overlay
        document.querySelectorAll('.fixed').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal);
                }
            });
        });
    }

    // =====================================
    // AUTHENTIFICATION
    // =====================================

    async handleCodeLogin(e) {
        e.preventDefault();
        
        const submitBtn = e.target.querySelector('button[type="submit"]');
        const btnText = submitBtn.querySelector('.btn-text');
        const spinner = submitBtn.querySelector('.loading-spinner');
        
        // État de chargement
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;

        const code = document.getElementById('accessCode').value.trim().toUpperCase();
        console.log('🔍 Tentative de connexion avec code:', code);
        console.log('🔗 URL API:', this.API_BASE);

        try {
            console.log('📡 Envoi requête vers:', `${this.API_BASE}/auth/validate-code`);
            
            const response = await fetch(`${this.API_BASE}/auth/validate-code`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code })
            });

            console.log('📨 Réponse reçue, status:', response.status);
            
            const data = await response.json();
            console.log('📄 Données réponse:', data);

            if (response.ok) {
                this.token = data.token;
                this.currentVilla = data.villa;
                localStorage.setItem('villa_token', this.token);
                
                console.log('✅ Connexion réussie, villa:', data.villa.name);
                this.showNotification('Connexion réussie !', 'success');
                this.showDashboard();
            } else {
                console.log('❌ Erreur API:', data.message);
                this.showNotification(data.message || 'Code invalide', 'error');
            }
        } catch (error) {
            console.error('💥 Erreur fetch:', error);
            this.showNotification('Erreur de connexion. Vérifiez que le serveur backend est démarré sur le port 3002.', 'error');
        } finally {
            // Restaurer le bouton
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    async handleEmailLogin(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch(`${this.API_BASE}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.currentVilla = data.villa;
                localStorage.setItem('villa_token', this.token);
                
                this.showNotification('Connexion réussie !', 'success');
                this.showDashboard();
            } else {
                this.showNotification(data.message || 'Identifiants invalides', 'error');
            }
        } catch (error) {
            console.error('Erreur connexion email:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    async validateToken() {
        try {
            const response = await fetch(`${this.API_BASE}/auth/validate-token`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.currentVilla = data.villa;
                this.showDashboard();
            } else {
                throw new Error('Token invalide');
            }
        } catch (error) {
            this.logout();
            throw error;
        }
    }

    toggleEmailLogin() {
        const emailForm = document.getElementById('emailLoginForm');
        const showBtn = document.getElementById('showLoginForm');
        
        if (emailForm.classList.contains('hidden')) {
            emailForm.classList.remove('hidden');
            showBtn.textContent = 'Masquer';
        } else {
            emailForm.classList.add('hidden');
            showBtn.innerHTML = '<i class="fas fa-user mr-2"></i>Connexion Email/Mot de passe';
        }
    }

    validateCodeFormat(e) {
        let value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        e.target.value = value;
        
        // Validation visuelle
        const isValid = /^[A-Z0-9]{6}$/.test(value);
        if (value.length === 6) {
            if (isValid) {
                e.target.style.borderColor = '#10b981';
            } else {
                e.target.style.borderColor = '#ef4444';
            }
        } else {
            e.target.style.borderColor = '';
        }
    }

    logout() {
        localStorage.removeItem('villa_token');
        this.token = null;
        this.currentVilla = null;
        
        // Réinitialiser l'interface
        document.getElementById('loginPage').classList.remove('hidden');
        document.getElementById('adminDashboard').classList.add('hidden');
        document.getElementById('userInfo').classList.add('hidden');
        
        // Réinitialiser les formulaires
        document.getElementById('codeForm').reset();
        document.getElementById('emailLoginForm').reset();
        document.getElementById('emailLoginForm').classList.add('hidden');
        
        this.showNotification('Déconnexion réussie', 'success');
    }

    // =====================================
    // INTERFACE DASHBOARD
    // =====================================

    async showDashboard() {
        // Masquer login, afficher dashboard
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('adminDashboard').classList.remove('hidden');
        document.getElementById('userInfo').classList.remove('hidden');

        // Mettre à jour les infos villa
        this.updateVillaInfo();
        
        // Charger les données
        await this.loadDashboardData();
        
        // Initialiser le calendrier
        this.initializeCalendar();
    }

    updateVillaInfo() {
        if (!this.currentVilla) return;

        document.getElementById('villaName').textContent = this.currentVilla.name;
        document.getElementById('dashboardVillaName').textContent = this.currentVilla.name;
        document.getElementById('villaLocation').textContent = this.currentVilla.location;
        
        if (this.currentVilla.image) {
            document.getElementById('villaImage').src = this.currentVilla.image;
        }
        
        document.getElementById('lastUpdate').textContent = 
            `Dernière mise à jour: ${new Date().toLocaleString('fr-FR')}`;
    }

    async loadDashboardData() {
        try {
            // Charger les statistiques
            await this.loadStats();
            
            // Charger les réservations
            await this.loadReservations();
            
        } catch (error) {
            console.error('Erreur chargement dashboard:', error);
            this.showNotification('Erreur de chargement des données', 'error');
        }
    }

    async loadStats() {
        try {
            const response = await fetch(`${this.API_BASE}/villa/stats`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const stats = await response.json();
                
                document.getElementById('availableDays').textContent = stats.availableDays || 0;
                document.getElementById('bookedDays').textContent = stats.bookedDays || 0;
                document.getElementById('blockedDays').textContent = stats.blockedDays || 0;
                document.getElementById('totalRevenue').textContent = `${stats.totalRevenue || 0}€`;
            }
        } catch (error) {
            console.error('Erreur chargement stats:', error);
        }
    }

    async loadReservations() {
        try {
            const response = await fetch(`${this.API_BASE}/villa/reservations`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const reservations = await response.json();
                this.displayReservations(reservations);
            }
        } catch (error) {
            console.error('Erreur chargement réservations:', error);
        }
    }

    displayReservations(reservations) {
        const tbody = document.getElementById('reservationsTable');
        
        if (!reservations || reservations.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center py-8 text-white/60">
                        <i class="fas fa-inbox mr-2"></i>Aucune réservation récente
                    </td>
                </tr>
            `;
            return;
        }

        tbody.innerHTML = reservations.map(reservation => `
            <tr class="border-b border-white/5 hover:bg-white/5">
                <td class="py-3 px-4">
                    <div class="font-semibold">${reservation.client_name || 'Client'}</div>
                    <div class="text-sm text-white/60">${reservation.client_email || ''}</div>
                </td>
                <td class="py-3 px-4">
                    <div class="font-semibold">${this.formatDate(reservation.checkin_date)}</div>
                    <div class="text-sm text-white/60">au ${this.formatDate(reservation.checkout_date)}</div>
                </td>
                <td class="py-3 px-4">
                    <span class="px-2 py-1 rounded-full text-xs font-semibold ${this.getStatusClass(reservation.status)}">
                        ${this.getStatusText(reservation.status)}
                    </span>
                </td>
                <td class="py-3 px-4 font-semibold">
                    ${reservation.total_amount || 0}€
                </td>
                <td class="py-3 px-4">
                    <button onclick="adminApp.viewReservation('${reservation.id}')" 
                            class="text-yellow-400 hover:text-yellow-300">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    // =====================================
    // CALENDRIER
    // =====================================

    initializeCalendar() {
        const calendarEl = document.getElementById('calendar');
        
        this.calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'fr',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,dayGridWeek'
            },
            buttonText: {
                today: 'Aujourd\'hui',
                month: 'Mois',
                week: 'Semaine'
            },
            height: 'auto',
            selectable: true,
            selectMirror: true,
            select: (info) => this.handleDateSelect(info),
            eventClick: (info) => this.handleEventClick(info),
            events: (info, successCallback, failureCallback) => {
                this.loadCalendarEvents(info, successCallback, failureCallback);
            },
            eventDidMount: (info) => {
                // Personnaliser l'affichage des événements
                info.el.setAttribute('title', info.event.extendedProps.description || '');
            }
        });

        this.calendar.render();
    }

    async loadCalendarEvents(info, successCallback, failureCallback) {
        try {
            const response = await fetch(`${this.API_BASE}/villa/calendar?start=${info.startStr}&end=${info.endStr}`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const events = await response.json();
                successCallback(events);
            } else {
                failureCallback();
            }
        } catch (error) {
            console.error('Erreur chargement événements calendrier:', error);
            failureCallback();
        }
    }

    handleDateSelect(info) {
        // Ouvrir modal pour ajouter disponibilité
        document.getElementById('startDate').value = info.startStr;
        document.getElementById('endDate').value = info.end ? 
            new Date(info.end.getTime() - 24 * 60 * 60 * 1000).toISOString().split('T')[0] : 
            info.startStr;
        
        this.showAvailabilityModal();
        
        // Désélectionner
        this.calendar.unselect();
    }

    handleEventClick(info) {
        const event = info.event;
        const eventType = event.extendedProps.type;
        
        if (eventType === 'blocked') {
            if (confirm('Voulez-vous débloquer ces dates ?')) {
                this.removeEvent(event.id);
            }
        } else if (eventType === 'available') {
            if (confirm('Voulez-vous supprimer cette disponibilité ?')) {
                this.removeEvent(event.id);
            }
        } else if (eventType === 'booked') {
            this.showNotification('Cette période est réservée et ne peut pas être modifiée', 'error');
        }
    }

    async removeEvent(eventId) {
        try {
            const response = await fetch(`${this.API_BASE}/villa/availability/${eventId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.calendar.refetchEvents();
                this.loadStats(); // Recharger les statistiques
                this.showNotification('Événement supprimé avec succès', 'success');
            } else {
                this.showNotification('Erreur lors de la suppression', 'error');
            }
        } catch (error) {
            console.error('Erreur suppression événement:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    // =====================================
    // MODALS ET FORMULAIRES
    // =====================================

    showAvailabilityModal() {
        const modal = document.getElementById('availabilityModal');
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        
        // Pré-remplir le prix si disponible
        if (this.currentVilla && this.currentVilla.default_price) {
            document.getElementById('pricePerNight').value = this.currentVilla.default_price;
        }
    }

    showBlockModal() {
        const modal = document.getElementById('blockModal');
        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    closeModal(modal) {
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            
            // Reset forms
            const forms = modal.querySelectorAll('form');
            forms.forEach(form => form.reset());
        }
    }

    async handleAvailabilitySubmit(e) {
        e.preventDefault();
        
        const formData = {
            start_date: document.getElementById('startDate').value,
            end_date: document.getElementById('endDate').value,
            price_per_night: parseFloat(document.getElementById('pricePerNight').value),
            notes: document.getElementById('availabilityNotes').value,
            type: 'available'
        };

        try {
            const response = await fetch(`${this.API_BASE}/villa/availability`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.closeModal(document.getElementById('availabilityModal'));
                this.calendar.refetchEvents();
                this.loadStats();
                this.showNotification('Disponibilité ajoutée avec succès !', 'success');
            } else {
                const error = await response.json();
                this.showNotification(error.message || 'Erreur lors de l\'ajout', 'error');
            }
        } catch (error) {
            console.error('Erreur ajout disponibilité:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    async handleBlockSubmit(e) {
        e.preventDefault();
        
        const formData = {
            start_date: document.getElementById('blockStartDate').value,
            end_date: document.getElementById('blockEndDate').value,
            reason: document.getElementById('blockReason').value,
            notes: document.getElementById('blockNotes').value,
            type: 'blocked'
        };

        try {
            const response = await fetch(`${this.API_BASE}/villa/availability`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                this.closeModal(document.getElementById('blockModal'));
                this.calendar.refetchEvents();
                this.loadStats();
                this.showNotification('Dates bloquées avec succès !', 'success');
            } else {
                const error = await response.json();
                this.showNotification(error.message || 'Erreur lors du blocage', 'error');
            }
        } catch (error) {
            console.error('Erreur blocage dates:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    // =====================================
    // FONCTIONNALITÉS AVANCÉES
    // =====================================

    async editVilla() {
        // Implémentation simplifiée - pourrait ouvrir une modal d'édition
        this.showNotification('Fonctionnalité d\'édition en cours de développement', 'info');
    }

    async exportCalendar() {
        try {
            const response = await fetch(`${this.API_BASE}/villa/export-calendar`, {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `calendrier-${this.currentVilla.code}-${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showNotification('Export CSV généré avec succès !', 'success');
            } else {
                this.showNotification('Erreur lors de l\'export', 'error');
            }
        } catch (error) {
            console.error('Erreur export:', error);
            this.showNotification('Erreur de connexion', 'error');
        }
    }

    viewReservation(reservationId) {
        // Implémentation simplifiée - pourrait ouvrir une modal avec détails
        this.showNotification(`Affichage détails réservation ${reservationId}`, 'info');
    }

    // =====================================
    // UTILITAIRES
    // =====================================

    showNotification(message, type = 'info') {
        const container = document.getElementById('notificationContainer');
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        const icon = type === 'success' ? 'fa-check-circle' : 
                    type === 'error' ? 'fa-exclamation-circle' : 
                    'fa-info-circle';
        
        notification.innerHTML = `
            <i class="fas ${icon} mr-2"></i>
            ${message}
        `;
        
        container.appendChild(notification);
        
        // Animer l'entrée
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Supprimer après 5 secondes
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 5000);
    }

    formatDate(dateString) {
        if (!dateString) return '--';
        return new Date(dateString).toLocaleDateString('fr-FR');
    }

    getStatusClass(status) {
        switch (status) {
            case 'confirmed': return 'bg-green-500 text-white';
            case 'pending': return 'bg-yellow-500 text-black';
            case 'cancelled': return 'bg-red-500 text-white';
            default: return 'bg-gray-500 text-white';
        }
    }

    getStatusText(status) {
        switch (status) {
            case 'confirmed': return 'Confirmé';
            case 'pending': return 'En attente';
            case 'cancelled': return 'Annulé';
            default: return 'Inconnu';
        }
    }

    initializeVideoBackground() {
        const video = document.getElementById('backgroundVideo');
        if (video) {
            // Même logique que index.html pour iOS
            const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
            
            if (isIOS) {
                video.setAttribute('webkit-playsinline', '');
                video.setAttribute('playsinline', '');
                video.muted = true;
                video.defaultMuted = true;
                video.volume = 0;
                
                video.play().catch(() => {
                    const startVideo = () => {
                        video.play().then(() => {
                            document.removeEventListener('touchstart', startVideo);
                            document.removeEventListener('click', startVideo);
                        });
                    };
                    
                    document.addEventListener('touchstart', startVideo, { once: true });
                    document.addEventListener('click', startVideo, { once: true });
                });
            } else {
                video.play().catch(error => {
                    console.log('Autoplay bloqué:', error);
                });
            }
        }
    }
}

// Initialisation globale
let adminApp;
document.addEventListener('DOMContentLoaded', function() {
    adminApp = new AdminProprietaires();
});

// Export pour utilisation externe
window.AdminProprietaires = AdminProprietaires;