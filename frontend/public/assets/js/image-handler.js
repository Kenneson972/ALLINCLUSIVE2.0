// Image Handler - Gestion des uploads et galerie d'images

class ImageHandler {
    constructor(app) {
        this.app = app;
        this.uploadedImages = JSON.parse(localStorage.getItem('admin_images')) || [];
        this.setupImageUpload();
    }

    setupImageUpload() {
        const uploadArea = document.getElementById('uploadArea');
        const fileInput = document.getElementById('imageUpload');
        const villaSelector = document.getElementById('villaSelector');

        if (!uploadArea || !fileInput) return;

        // Setup villa selector
        if (villaSelector) {
            this.populateVillaSelector();
            villaSelector.addEventListener('change', (e) => {
                this.selectVilla(e.target.value);
            });
        }

        // Drag and drop events
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            this.handleFiles(files);
        });

        // File input change event
        fileInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            this.handleFiles(files);
        });

        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
    }

    populateVillaSelector() {
        const selector = document.getElementById('villaSelector');
        if (!selector || !this.app.villas) return;

        // Clear existing options except "All villas"
        selector.innerHTML = '<option value="">Toutes les villas</option>';

        // Add villa options
        this.app.villas.forEach(villa => {
            const option = document.createElement('option');
            option.value = villa.id;
            option.textContent = `${villa.name} (${villa.photos ? villa.photos.length : 0} photos)`;
            selector.appendChild(option);
        });
    }

    selectVilla(villaId) {
        const selectedVillaInfo = document.getElementById('selectedVillaInfo');
        
        if (!villaId) {
            selectedVillaInfo.style.display = 'none';
            this.selectedVilla = null;
            this.loadImageGallery();
            return;
        }

        const villa = this.app.villas.find(v => v.id == villaId);
        if (!villa) return;

        this.selectedVilla = villa;
        window.selectedVillaId = villa.id; // For global access

        // Update villa info display
        document.getElementById('selectedVillaName').textContent = villa.name;
        document.getElementById('selectedVillaLocation').textContent = villa.location;
        document.getElementById('selectedVillaDescription').textContent = villa.description.substring(0, 100) + '...';
        document.getElementById('selectedVillaPrice').textContent = villa.price + '€/nuit';
        document.getElementById('selectedVillaDetails').textContent = `${villa.capacity} personnes • ${villa.bedrooms || 0} chambres`;
        
        selectedVillaInfo.style.display = 'block';

        // Filter images for this villa
        this.loadImageGallery(villaId);
    }

    async handleFiles(files) {
        const imageFiles = files.filter(file => file.type.startsWith('image/'));
        
        if (imageFiles.length === 0) {
            this.app.showToast('Veuillez sélectionner des fichiers images valides', 'error');
            return;
        }

        this.app.showToast(`Upload de ${imageFiles.length} images en cours...`, 'info');

        for (const file of imageFiles) {
            try {
                await this.uploadImage(file);
            } catch (error) {
                console.error('Erreur upload:', error);
                this.app.showToast(`Erreur lors de l'upload de ${file.name}`, 'error');
            }
        }

        this.saveImages();
        this.loadImageGallery();
        this.app.showToast(`${imageFiles.length} images uploadées avec succès`, 'success');
    }

    async uploadImage(file) {
        return new Promise((resolve, reject) => {
            // Validate file size (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                reject(new Error('Fichier trop volumineux (max 5MB)'));
                return;
            }

            // Validate file type
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
            if (!allowedTypes.includes(file.type)) {
                reject(new Error('Type de fichier non supporté'));
                return;
            }

            const reader = new FileReader();
            
            reader.onload = (e) => {
                try {
                    // Create image object
                    const img = new Image();
                    img.onload = () => {
                        // Compress and resize if needed
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');
                        
                        // Calculate new dimensions (max 1200px width)
                        let { width, height } = img;
                        const maxWidth = 1200;
                        
                        if (width > maxWidth) {
                            height = (height * maxWidth) / width;
                            width = maxWidth;
                        }
                        
                        canvas.width = width;
                        canvas.height = height;
                        
                        // Draw and compress
                        ctx.drawImage(img, 0, 0, width, height);
                        const compressedDataUrl = canvas.toDataURL('image/jpeg', 0.8);
                        
                        // Generate filename
                        const fileName = this.generateImageName(file.name);
                        
                        // Store image
                        const imageData = {
                            id: this.generateImageId(),
                            name: fileName,
                            originalName: file.name,
                            dataUrl: compressedDataUrl,
                            size: file.size,
                            type: file.type,
                            width: width,
                            height: height,
                            uploaded: new Date().toISOString()
                        };
                        
                        this.uploadedImages.push(imageData);
                        resolve(imageData);
                    };
                    
                    img.onerror = () => reject(new Error('Impossible de charger l\'image'));
                    img.src = e.target.result;
                    
                } catch (error) {
                    reject(error);
                }
            };
            
            reader.onerror = () => reject(new Error('Erreur de lecture du fichier'));
            reader.readAsDataURL(file);
        });
    }

    loadImageGallery(villaId = null) {
        const gallery = document.getElementById('imageGallery');
        if (!gallery) return;

        // Populate villa selector if not done
        this.populateVillaSelector();

        let imagesToShow = this.uploadedImages;

        // Filter by villa if specified
        if (villaId) {
            // Show images from this specific villa
            const villa = this.app.villas.find(v => v.id == villaId);
            if (villa && villa.photos) {
                // Convert villa photos to image format for display
                imagesToShow = villa.photos.map((photo, index) => ({
                    id: `villa_${villaId}_${index}`,
                    name: `${villa.name} - ${index + 1}`,
                    dataUrl: photo,
                    size: 0,
                    type: 'image/jpeg',
                    width: 300,
                    height: 200,
                    uploaded: villa.updated,
                    villaId: villaId,
                    isVillaPhoto: true
                }));
            }
        }

        if (imagesToShow.length === 0) {
            gallery.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-images fa-3x text-muted mb-3"></i>
                    <h5>${villaId ? 'Aucune image pour cette villa' : 'Aucune image'}</h5>
                    <p class="text-muted">${villaId ? 'Cette villa n\'a pas encore d\'images' : 'Uploadez vos premières images pour commencer'}</p>
                    ${villaId ? `<button class="btn btn-primary" onclick="document.getElementById('imageUpload').click()">
                        <i class="fas fa-plus me-2"></i>Ajouter des images à cette villa
                    </button>` : ''}
                </div>
            `;
            return;
        }

        // Sort by upload date (newest first)
        const sortedImages = imagesToShow
            .sort((a, b) => new Date(b.uploaded) - new Date(a.uploaded));

        gallery.innerHTML = sortedImages.map(image => `
            <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                <div class="image-item">
                    <img src="${image.dataUrl}" alt="${image.name}" class="img-fluid">
                    <div class="image-overlay">
                        <div class="btn-group">
                            <button class="btn btn-sm btn-light" onclick="imageHandler.previewImage('${image.id}')" title="Aperçu">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-success" onclick="imageHandler.copyImageUrl('${image.id}')" title="Copier URL">
                                <i class="fas fa-copy"></i>
                            </button>
                            ${image.isVillaPhoto ? 
                                `<button class="btn btn-sm btn-warning" onclick="imageHandler.removeFromVilla('${image.id}')" title="Retirer de la villa">
                                    <i class="fas fa-unlink"></i>
                                </button>` :
                                `<button class="btn btn-sm btn-info" onclick="imageHandler.assignToVilla('${image.id}')" title="Assigner à villa">
                                    <i class="fas fa-link"></i>
                                </button>`
                            }
                            <button class="btn btn-sm btn-danger" onclick="imageHandler.deleteImage('${image.id}')" title="Supprimer">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                    <div class="image-info mt-2">
                        <small class="text-muted d-block">${image.name}</small>
                        <small class="text-muted">
                            ${this.formatFileSize(image.size)} 
                            ${image.width && image.height ? `• ${image.width}×${image.height}` : ''}
                        </small>
                        ${image.villaId ? `<div><span class="badge bg-primary mt-1">Villa ID: ${image.villaId}</span></div>` : ''}
                    </div>
                </div>
            </div>
        `).join('');
    }

    previewImage(imageId) {
        const image = this.uploadedImages.find(img => img.id === imageId);
        if (!image) return;

        // Create preview modal
        const modalHtml = `
            <div class="modal fade" id="imagePreviewModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${image.name}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${image.dataUrl}" alt="${image.name}" class="img-fluid" style="max-height: 70vh;">
                            <div class="mt-3">
                                <p class="mb-1"><strong>Nom:</strong> ${image.originalName}</p>
                                <p class="mb-1"><strong>Taille:</strong> ${this.formatFileSize(image.size)}</p>
                                <p class="mb-1"><strong>Dimensions:</strong> ${image.width}×${image.height}px</p>
                                <p class="mb-1"><strong>Uploadé:</strong> ${new Date(image.uploaded).toLocaleString('fr-FR')}</p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-success" onclick="imageHandler.copyImageUrl('${image.id}')">
                                <i class="fas fa-copy me-2"></i>Copier URL
                            </button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Remove existing modal if any
        const existingModal = document.getElementById('imagePreviewModal');
        if (existingModal) {
            existingModal.remove();
        }

        // Add modal to body
        document.body.insertAdjacentHTML('beforeend', modalHtml);

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
        modal.show();

        // Clean up modal after hide
        document.getElementById('imagePreviewModal').addEventListener('hidden.bs.modal', () => {
            document.getElementById('imagePreviewModal').remove();
        });
    }

    copyImageUrl(imageId) {
        const image = this.uploadedImages.find(img => img.id === imageId);
        if (!image) return;

        // For now, copy the data URL. In a real scenario, this would be a proper URL
        navigator.clipboard.writeText(image.dataUrl).then(() => {
            this.app.showToast('URL d\'image copiée dans le presse-papiers', 'success');
        }).catch(() => {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = image.dataUrl;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            this.app.showToast('URL d\'image copiée dans le presse-papiers', 'success');
        });
    }

    deleteImage(imageId) {
        const image = this.uploadedImages.find(img => img.id === imageId);
        if (!image) return;

        if (confirm(`Supprimer l'image "${image.name}" ? Cette action est irréversible.`)) {
            this.uploadedImages = this.uploadedImages.filter(img => img.id !== imageId);
            this.saveImages();
            this.loadImageGallery();
            this.app.showToast('Image supprimée avec succès', 'success');
        }
    }

    generateImageId() {
        return 'img_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    generateImageName(originalName) {
        const timestamp = new Date().toISOString().split('T')[0].replace(/-/g, '');
        const randomStr = Math.random().toString(36).substr(2, 5);
        const extension = originalName.split('.').pop();
        return `villa-${timestamp}-${randomStr}.${extension}`;
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    saveImages() {
        localStorage.setItem('admin_images', JSON.stringify(this.uploadedImages));
    }

    // Get images for villa selection
    getImagesForSelect() {
        return this.uploadedImages.map(img => ({
            id: img.id,
            name: img.name,
            url: img.dataUrl,
            thumbnail: img.dataUrl // Same for now, could generate thumbnails
        }));
    }

    // Bulk operations
    bulkDeleteImages(imageIds) {
        if (confirm(`Supprimer ${imageIds.length} images ? Cette action est irréversible.`)) {
            this.uploadedImages = this.uploadedImages.filter(img => !imageIds.includes(img.id));
            this.saveImages();
            this.loadImageGallery();
            this.app.showToast(`${imageIds.length} images supprimées`, 'success');
        }
    }

    // Image optimization
    optimizeImage(imageData, maxWidth = 1200, quality = 0.8) {
        return new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                
                // Calculate dimensions
                let { width, height } = img;
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                // Draw and compress
                ctx.drawImage(img, 0, 0, width, height);
                const optimizedDataUrl = canvas.toDataURL('image/jpeg', quality);
                
                resolve({
                    dataUrl: optimizedDataUrl,
                    width: width,
                    height: height
                });
            };
            img.src = imageData;
        });
    }

    // Export images data
    exportImages() {
        const data = {
            images: this.uploadedImages,
            exported: new Date().toISOString(),
            total: this.uploadedImages.length
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `khanelconcept-images-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.app.showToast('Images exportées avec succès', 'success');
    }

    // Import images data
    importImages() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = (event) => {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    try {
                        const data = JSON.parse(e.target.result);
                        if (data.images && Array.isArray(data.images)) {
                            if (confirm(`Importer ${data.images.length} images ? Cela ajoutera aux images existantes.`)) {
                                this.uploadedImages = [...this.uploadedImages, ...data.images];
                                this.saveImages();
                                this.loadImageGallery();
                                this.app.showToast(`${data.images.length} images importées avec succès`, 'success');
                            }
                        } else {
                            this.app.showToast('Format de fichier invalide', 'error');
                        }
                    } catch (error) {
                        this.app.showToast('Erreur lors de la lecture du fichier', 'error');
                    }
                };
                reader.readAsText(file);
            }
        };
        input.click();
    }
}

// Global image handler instance
let imageHandler;