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
    formatPrice
};