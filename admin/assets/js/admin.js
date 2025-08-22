// ================================
// KhanelConcept Admin Panel JS
// ================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Animation des cards au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observer toutes les cards
    document.querySelectorAll('.glass-card, .stat-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Gestion du menu mobile
    const mobileToggle = document.querySelector('.mobile-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }

    // Fermer le menu mobile en cliquant à l'extérieur
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !mobileToggle?.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        }
    });

    // Confirmation de suppression
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm-delete') || 'Êtes-vous sûr de vouloir supprimer cet élément ?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss pour les alertes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });

    // Gestion des formulaires avec validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
});

// Validation de formulaire
function validateForm(form) {
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'Ce champ est obligatoire');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    return isValid;
}

// Afficher erreur sur un champ
function showFieldError(field, message) {
    clearFieldError(field);
    
    const error = document.createElement('div');
    error.className = 'field-error';
    error.style.color = '#dc3545';
    error.style.fontSize = '0.8rem';
    error.style.marginTop = '0.25rem';
    error.textContent = message;
    
    field.parentNode.appendChild(error);
    field.style.borderColor = '#dc3545';
}

// Effacer erreur d'un champ
function clearFieldError(field) {
    const existingError = field.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    field.style.borderColor = '';
}

// Gestion upload d'images avec drag & drop
function initImageUpload(dropZone, fileInput, callback) {
    if (!dropZone || !fileInput) return;
    
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    const maxSize = 5 * 1024 * 1024; // 5MB
    
    // Drag & Drop
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files);
        processFiles(files);
    });
    
    // Clic sur la zone
    dropZone.addEventListener('click', function() {
        fileInput.click();
    });
    
    // Sélection via input
    fileInput.addEventListener('change', function() {
        const files = Array.from(this.files);
        processFiles(files);
    });
    
    function processFiles(files) {
        files.forEach(file => {
            if (!allowedTypes.includes(file.type)) {
                alert(`Type de fichier non autorisé : ${file.name}`);
                return;
            }
            
            if (file.size > maxSize) {
                alert(`Fichier trop volumineux : ${file.name} (max 5MB)`);
                return;
            }
            
            if (callback) {
                callback(file);
            }
        });
    }
}

// Preview d'image
function previewImage(file, container) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.maxWidth = '200px';
        img.style.maxHeight = '200px';
        img.style.borderRadius = '8px';
        img.style.objectFit = 'cover';
        
        const preview = document.createElement('div');
        preview.className = 'image-preview';
        preview.style.position = 'relative';
        preview.style.display = 'inline-block';
        preview.style.margin = '0.5rem';
        
        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = '<i class="fas fa-times"></i>';
        removeBtn.style.position = 'absolute';
        removeBtn.style.top = '-8px';
        removeBtn.style.right = '-8px';
        removeBtn.style.background = '#dc3545';
        removeBtn.style.color = 'white';
        removeBtn.style.border = 'none';
        removeBtn.style.borderRadius = '50%';
        removeBtn.style.width = '24px';
        removeBtn.style.height = '24px';
        removeBtn.style.cursor = 'pointer';
        removeBtn.style.fontSize = '0.7rem';
        
        removeBtn.addEventListener('click', function() {
            preview.remove();
        });
        
        preview.appendChild(img);
        preview.appendChild(removeBtn);
        container.appendChild(preview);
    };
    reader.readAsDataURL(file);
}

// Notification toast
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        color: white;
        z-index: 10000;
        transform: translateX(400px);
        transition: all 0.3s ease;
    `;
    
    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
    toast.innerHTML = `<i class="fas fa-${icon}"></i> ${message}`;
    
    document.body.appendChild(toast);
    
    // Animation d'entrée
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto-remove
    setTimeout(() => {
        toast.style.transform = 'translateX(400px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Chargement dynamique avec spinner
function showLoading(element, text = 'Chargement...') {
    const loader = document.createElement('div');
    loader.className = 'loading-overlay';
    loader.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        z-index: 100;
    `;
    loader.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`;
    
    element.style.position = 'relative';
    element.appendChild(loader);
}

function hideLoading(element) {
    const loader = element.querySelector('.loading-overlay');
    if (loader) {
        loader.remove();
    }
}

// Fonction utilitaire pour formater les nombres
function formatNumber(number) {
    return new Intl.NumberFormat('fr-FR').format(number);
}

// Fonction utilitaire pour formater les prix
function formatPrice(price) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price);
}

// Auto-génération de slug
function generateSlug(text) {
    return text
        .toLowerCase()
        .replace(/[àâäã]/g, 'a')
        .replace(/[éèêë]/g, 'e')
        .replace(/[îï]/g, 'i')
        .replace(/[ôöõ]/g, 'o')
        .replace(/[ùûü]/g, 'u')
        .replace(/[ç]/g, 'c')
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/[\s-]+/g, '-')
        .replace(/^-+|-+$/g, '');
}

// Initialiser l'auto-génération de slug
document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.querySelector('#nom');
    const slugInput = document.querySelector('#slug');
    
    if (nameInput && slugInput) {
        nameInput.addEventListener('input', function() {
            if (!slugInput.dataset.manual) {
                slugInput.value = generateSlug(this.value);
            }
        });
        
        slugInput.addEventListener('input', function() {
            this.dataset.manual = 'true';
        });
    }
});

// ================================
// FONCTIONS GÉNÉRATEUR DE PAGES
// ================================

// Générer une page villa (pour modifier.php)
async function generateVillaPage() {
    const villaId = document.getElementById('villa_id')?.value || 
                   new URLSearchParams(window.location.search).get('id');
    
    if (!villaId) {
        showToast('❌ ID villa manquant', 'error');
        return;
    }
    
    showLoadingState('Génération de la page HTML...');
    
    try {
        const response = await fetch('/admin/villas/generer_pages.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                action: 'generate_single',
                villa_id: villaId 
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('✅ Page HTML générée avec succès !', 'success');
            
            // Afficher modal avec lien vers la page générée
            showPageGenerationModal({
                title: 'Page Villa Générée !',
                message: 'Votre page villa est maintenant disponible :',
                pageUrl: result.page_url,
                villaName: result.villa_name || 'Villa'
            });
            
            // Mettre à jour le statut si présent
            updateGenerationStatus(true);
            
        } else {
            showToast('❌ ' + (result.error || 'Erreur lors de la génération'), 'error');
        }
    } catch (error) {
        console.error('Erreur génération:', error);
        showToast('❌ Erreur lors de la génération', 'error');
    } finally {
        hideLoadingState();
    }
}

// Générer toutes les pages (pour dashboard)
async function generateAllPages() {
    const progressContainer = document.getElementById('generation-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const resultsContainer = document.getElementById('generation-results');
    
    // Afficher le progress
    if (progressContainer) {
        progressContainer.style.display = 'block';
        resultsContainer && (resultsContainer.style.display = 'none');
        progressFill && (progressFill.style.width = '0%');
        progressText && (progressText.textContent = 'Initialisation de la génération...');
    } else {
        showLoadingState('Génération de toutes les pages en cours...');
    }
    
    try {
        // Simulation du progrès
        if (progressFill && progressText) {
            progressFill.style.width = '20%';
            progressText.textContent = 'Récupération des villas...';
        }
        
        const response = await fetch('/admin/villas/generer_pages.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                action: 'generate_all'
            })
        });
        
        if (progressFill && progressText) {
            progressFill.style.width = '80%';
            progressText.textContent = 'Génération des pages en cours...';
        }
        
        const result = await response.json();
        
        if (progressFill && progressText) {
            progressFill.style.width = '100%';
            progressText.textContent = 'Génération terminée !';
        }
        
        // Afficher les résultats
        setTimeout(() => {
            if (resultsContainer && typeof displayResults === 'function') {
                displayResults(result);
                progressContainer && (progressContainer.style.display = 'none');
            } else {
                // Fallback pour dashboard simple
                if (result.success) {
                    showToast(`✅ ${result.generated?.length || 0} pages générées avec succès !`, 'success');
                } else {
                    showToast('❌ Erreur lors de la génération', 'error');
                }
            }
        }, 1000);
        
    } catch (error) {
        console.error('Erreur génération:', error);
        if (progressText && progressFill) {
            progressText.textContent = 'Erreur lors de la génération';
            progressFill.style.width = '100%';
            progressFill.style.background = '#dc3545';
        } else {
            showToast('❌ Erreur lors de la génération de toutes les pages', 'error');
        }
    } finally {
        if (!progressContainer) {
            hideLoadingState();
        }
    }
}

// Afficher état de chargement pour génération
function showLoadingState(message) {
    const saveStatus = document.getElementById('save-status');
    if (saveStatus) {
        saveStatus.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${message}`;
        saveStatus.style.color = 'rgba(255,255,255,0.8)';
    }
}

// Masquer état de chargement
function hideLoadingState() {
    const saveStatus = document.getElementById('save-status');
    if (saveStatus) {
        saveStatus.innerHTML = '<i class="fas fa-check-circle" style="color: #28a745;"></i> Sauvegardé';
        saveStatus.style.color = 'rgba(255,255,255,0.8)';
    }
}

// Mettre à jour le statut de génération
function updateGenerationStatus(generated) {
    const saveStatus = document.getElementById('save-status');
    if (saveStatus && generated) {
        saveStatus.innerHTML = `
            <i class="fas fa-check-circle" style="color: #28a745;"></i> Sauvegardé
            <span style="margin-left: 1rem; color: #17a2b8;">
                <i class="fas fa-globe"></i> Page HTML générée
            </span>
        `;
    }
}

// Modal personnalisée pour affichage des résultats de génération
function showPageGenerationModal(options) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        opacity: 0;
        transition: opacity 0.3s ease;
    `;
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        text-align: center;
        color: white;
        transform: scale(0.9);
        transition: transform 0.3s ease;
    `;
    
    modalContent.innerHTML = `
        <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
        <h3 style="margin-bottom: 1rem; color: white;">${options.title}</h3>
        <p style="margin-bottom: 2rem; color: rgba(255,255,255,0.9);">${options.message}</p>
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <a href="${options.pageUrl}" target="_blank" 
               style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 0.75rem 1.5rem; text-decoration: none; 
                      border-radius: 8px; font-weight: 600;">
                🌐 Voir la Page
            </a>
            <button onclick="this.closest('.modal-overlay').remove()" 
                    style="background: rgba(255,255,255,0.1); color: white; 
                           border: 1px solid rgba(255,255,255,0.3); padding: 0.75rem 1.5rem; 
                           border-radius: 8px; cursor: pointer;">
                Fermer
            </button>
        </div>
    `;
    
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // Animation d'entrée
    setTimeout(() => {
        modal.style.opacity = '1';
        modalContent.style.transform = 'scale(1)';
    }, 10);
    
    // Fermer en cliquant à l'extérieur
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// Export des fonctions globales
window.AdminPanel = {
    showToast,
    showLoading,
    hideLoading,
    validateForm,
    initImageUpload,
    previewImage,
    generateSlug,
    formatNumber,
    formatPrice,
    generateVillaPage,
    generateAllPages
};