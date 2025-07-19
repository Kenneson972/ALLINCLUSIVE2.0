import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import flatpickr from 'flatpickr';
import 'flatpickr/dist/l10n/fr.js';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001/api';

function App() {
  // États pour les données
  const [villas, setVillas] = useState([]);
  const [filteredVillas, setFilteredVillas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentSection, setCurrentSection] = useState('home');
  
  // États pour la vue détaillée des villas
  const [showVillaDetail, setShowVillaDetail] = useState(false);
  const [selectedVilla, setSelectedVilla] = useState(null);
  
  // États pour la réservation
  const [showReservationModal, setShowReservationModal] = useState(false);
  const [currentVilla, setCurrentVilla] = useState(null);
  const [reservationData, setReservationData] = useState({
    customerName: '',
    customerEmail: '',
    customerPhone: '',
    checkinDate: '',
    checkoutDate: '',
    guestsCount: '',
    message: ''
  });
  
  // États pour la galerie
  const [showGalleryModal, setShowGalleryModal] = useState(false);
  const [currentGallery, setCurrentGallery] = useState([]);
  const [currentGalleryIndex, setCurrentGalleryIndex] = useState(0);
  
  // États pour la recherche
  const [searchFilters, setSearchFilters] = useState({
    destination: '',
    checkin: '',
    checkout: '',
    guests: '',
    category: 'all'
  });
  
  // États pour les messages
  const [statusMessage, setStatusMessage] = useState({ text: '', type: '' });
  
  // Références pour les calendriers
  const checkinRef = React.useRef();
  const checkoutRef = React.useRef();
  const modalCheckinRef = React.useRef();
  const modalCheckoutRef = React.useRef();

  // Chargement initial des villas
  useEffect(() => {
    const loadVillasData = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`${API_BASE_URL}/villas`);
        setVillas(response.data);
        setFilteredVillas(response.data);
        showStatusMessage('Bienvenue sur KhanelConcept ! Toutes les villas sont disponibles.', 'success');
      } catch (error) {
        console.error('Erreur lors du chargement des villas:', error);
        showStatusMessage('Erreur lors du chargement des villas.', 'error');
      } finally {
        setLoading(false);
      }
    };
    
    loadVillasData();
  }, []);

  // Script pour forcer le chargement vidéo Cloudinary
  useEffect(() => {
    const video = document.querySelector('.background-video');
    if (video) {
      console.log('🔍 Vidéo trouvée:', video);
      
      video.addEventListener('loadstart', () => console.log('🎬 loadstart'));
      video.addEventListener('loadedmetadata', () => console.log('📊 loadedmetadata'));
      video.addEventListener('loadeddata', () => console.log('📹 loadeddata'));
      video.addEventListener('canplay', () => console.log('✅ canplay'));
      video.addEventListener('canplaythrough', () => console.log('🚀 canplaythrough'));
      video.addEventListener('playing', () => console.log('▶️ playing'));
      video.addEventListener('error', (e) => {
        console.error('❌ Erreur vidéo:', e);
        console.error('Error details:', e.target.error);
      });

      // Forcer la lecture
      const playPromise = video.play();
      if (playPromise !== undefined) {
        playPromise
          .then(() => console.log('✅ Autoplay réussi !'))
          .catch((error) => console.error('❌ Autoplay échoué:', error));
      }
    } else {
      console.error('❌ Élément vidéo non trouvé !');
    }
  }, []);

  // Initialisation des calendriers
  useEffect(() => {
    if (checkinRef.current && checkoutRef.current) {
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);

      flatpickr(checkinRef.current, {
        locale: 'fr',
        minDate: today,
        dateFormat: 'd/m/Y',
        placeholder: 'Date d\'arrivée',
        onChange: function(selectedDates) {
          if (selectedDates[0]) {
            const nextDay = new Date(selectedDates[0]);
            nextDay.setDate(nextDay.getDate() + 1);
            setSearchFilters(prev => ({
              ...prev,
              checkin: selectedDates[0].toLocaleDateString('fr-FR')
            }));
          }
        }
      });

      flatpickr(checkoutRef.current, {
        locale: 'fr',
        minDate: tomorrow,
        dateFormat: 'd/m/Y',
        placeholder: 'Date de départ',
        onChange: function(selectedDates) {
          if (selectedDates[0]) {
            setSearchFilters(prev => ({
              ...prev,
              checkout: selectedDates[0].toLocaleDateString('fr-FR')
            }));
          }
        }
      });
    }
  }, []);

  // Initialisation des calendriers modaux
  useEffect(() => {
    if (modalCheckinRef.current && modalCheckoutRef.current && showReservationModal) {
      const today = new Date();
      const tomorrow = new Date(today);
      tomorrow.setDate(tomorrow.getDate() + 1);

      flatpickr(modalCheckinRef.current, {
        locale: 'fr',
        minDate: today,
        dateFormat: 'd/m/Y',
        placeholder: 'Date d\'arrivée',
        onChange: function(selectedDates) {
          if (selectedDates[0]) {
            setReservationData(prev => ({
              ...prev,
              checkinDate: selectedDates[0].toLocaleDateString('fr-FR')
            }));
          }
        }
      });

      flatpickr(modalCheckoutRef.current, {
        locale: 'fr',
        minDate: tomorrow,
        dateFormat: 'd/m/Y',
        placeholder: 'Date de départ',
        onChange: function(selectedDates) {
          if (selectedDates[0]) {
            setReservationData(prev => ({
              ...prev,
              checkoutDate: selectedDates[0].toLocaleDateString('fr-FR')
            }));
          }
        }
      });
    }
  }, [showReservationModal]);

  const showStatusMessage = (text, type) => {
    setStatusMessage({ text, type });
    setTimeout(() => {
      setStatusMessage({ text: '', type: '' });
    }, 3000);
  };

  const performSearch = async () => {
    showStatusMessage('Recherche en cours...', 'loading');
    
    try {
      const response = await axios.post(`${API_BASE_URL}/villas/search`, searchFilters);
      setFilteredVillas(response.data);
      
      if (response.data.length === 0) {
        showStatusMessage('Aucune villa trouvée pour ces critères. Essayez avec d\'autres paramètres.', 'error');
      } else {
        showStatusMessage(`${response.data.length} villa(s) trouvée(s) !`, 'success');
      }
    } catch (error) {
      console.error('Erreur lors de la recherche:', error);
      showStatusMessage('Erreur lors de la recherche.', 'error');
    }
  };

  const filterVillas = (category) => {
    setSearchFilters(prev => ({ ...prev, category }));
    
    let filtered = [...villas];
    
    if (category === 'all') {
      filtered = [...villas];
    } else if (category === 'pmr') {
      filtered = villas.filter(villa => 
        villa.features.toLowerCase().includes('accessible') || 
        villa.location.toLowerCase().includes('ste-luce') ||
        villa.guests <= 4
      );
    } else {
      filtered = villas.filter(villa => villa.category === category);
    }
    
    setFilteredVillas(filtered);
  };

  const openReservationModal = (villa) => {
    setCurrentVilla(villa);
    setReservationData({
      customerName: '',
      customerEmail: '',
      customerPhone: '',
      checkinDate: searchFilters.checkin || '',
      checkoutDate: searchFilters.checkout || '',
      guestsCount: searchFilters.guests || '',
      message: ''
    });
    setShowReservationModal(true);
  };

  const closeReservationModal = () => {
    setShowReservationModal(false);
    setCurrentVilla(null);
  };

  const handleReservationSubmit = async (e) => {
    e.preventDefault();
    
    if (!currentVilla) return;
    
    showStatusMessage('Traitement de votre réservation...', 'loading');
    
    try {
      const reservationPayload = {
        villa_id: currentVilla.id,
        customer_name: reservationData.customerName,
        customer_email: reservationData.customerEmail,
        customer_phone: reservationData.customerPhone,
        checkin_date: reservationData.checkinDate,
        checkout_date: reservationData.checkoutDate,
        guests_count: parseInt(reservationData.guestsCount),
        message: reservationData.message,
        total_price: calculateTotalPrice()
      };
      
      const response = await axios.post(`${API_BASE_URL}/reservations`, reservationPayload);
      
      if (response.data.success) {
        showStatusMessage('Réservation confirmée ! Un email de confirmation va vous être envoyé.', 'success');
        
        // Afficher un résumé détaillé
        alert(`✅ Réservation confirmée !

🏖️ Villa: ${currentVilla.name}
👤 Client: ${reservationData.customerName}
📧 Email: ${reservationData.customerEmail}
📞 Téléphone: ${reservationData.customerPhone}
📅 Du ${reservationData.checkinDate} au ${reservationData.checkoutDate}
👥 ${reservationData.guestsCount} voyageurs
💰 Total: ${calculateTotalPrice()}€

📧 Un email de confirmation va vous être envoyé avec tous les détails.
📞 Notre équipe vous contactera dans les plus brefs délais.`);
        
        closeReservationModal();
      }
    } catch (error) {
      console.error('Erreur lors de la réservation:', error);
      showStatusMessage('Erreur lors de la réservation. Veuillez réessayer.', 'error');
    }
  };

  const calculateTotalPrice = () => {
    if (!currentVilla || !reservationData.checkinDate || !reservationData.checkoutDate) return 0;
    
    const checkin = new Date(reservationData.checkinDate.split('/').reverse().join('-'));
    const checkout = new Date(reservationData.checkoutDate.split('/').reverse().join('-'));
    
    const nights = Math.ceil((checkout - checkin) / (1000 * 60 * 60 * 24));
    return nights > 0 ? nights * currentVilla.price : 0;
  };

  const openImageGallery = (villa, imageIndex = 0) => {
    if (!villa || !villa.gallery) return;
    
    setCurrentGallery(villa.gallery);
    setCurrentGalleryIndex(imageIndex);
    setShowGalleryModal(true);
  };

  const closeImageGallery = () => {
    setShowGalleryModal(false);
  };

  const previousImage = () => {
    setCurrentGalleryIndex((currentGalleryIndex - 1 + currentGallery.length) % currentGallery.length);
  };

  const nextImage = () => {
    setCurrentGalleryIndex((currentGalleryIndex + 1) % currentGallery.length);
  };

  const goToImage = (index) => {
    setCurrentGalleryIndex(index);
  };

  const showSection = (sectionId) => {
    setCurrentSection(sectionId);
  };

  const viewDetails = (villa) => {
    setSelectedVilla(villa);
    setShowVillaDetail(true);
  };

  const closeVillaDetail = () => {
    setShowVillaDetail(false);
    setSelectedVilla(null);
  };

  const openReservationFromDetail = (villa) => {
    setCurrentVilla(villa);
    setReservationData({
      customerName: '',
      customerEmail: '',
      customerPhone: '',
      checkinDate: searchFilters.checkin || '',
      checkoutDate: searchFilters.checkout || '',
      guestsCount: searchFilters.guests || '',
      message: ''
    });
    setShowReservationModal(true);
  };

  const contactPrestataire = (service) => {
    showStatusMessage(`Redirection vers ${service}...`, 'loading');
    
    setTimeout(() => {
      alert(`Service ${service}

Contactez-nous pour plus d'informations :
📞 +596 696 XX XX XX
📧 contact@khanelconcept.com`);
      showStatusMessage(`Contact ${service} - Formulaire affiché`, 'success');
    }, 1000);
  };

  const showComingSoon = () => {
    showStatusMessage('Fonctionnalité en cours de développement...', 'loading');
    
    setTimeout(() => {
      alert('Cette fonctionnalité sera bientôt disponible !\\n\\nRestez connecté pour les nouveautés.');
      showStatusMessage('Fonctionnalité à venir - Notification envoyée', 'success');
    }, 1000);
  };

  // Gestion des événements clavier
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (showGalleryModal) {
        if (e.key === 'ArrowLeft') {
          setCurrentGalleryIndex((prevIndex) => 
            (prevIndex - 1 + currentGallery.length) % currentGallery.length
          );
        }
        if (e.key === 'ArrowRight') {
          setCurrentGalleryIndex((prevIndex) => 
            (prevIndex + 1) % currentGallery.length
          );
        }
        if (e.key === 'Escape') closeImageGallery();
      }
      
      if (showReservationModal) {
        if (e.key === 'Escape') closeReservationModal();
      }
      
      if (showVillaDetail) {
        if (e.key === 'Escape') closeVillaDetail();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [showGalleryModal, showReservationModal, showVillaDetail, currentGallery.length]);

  return (
    <div className="App">
      {/* Cloudinary Background Video - Version qui fonctionnait */}
      <div className="video-background-loop">
        <video autoPlay muted loop playsInline className="background-video">
          <source src="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4" type="video/mp4" />
          Votre navigateur ne supporte pas la lecture de vidéos HTML5.
        </video>
        <div className="video-overlay"></div>
      </div>

      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo" onClick={() => showSection('home')}>
            <i className="fas fa-palm-tree"></i>
            KhanelConcept
          </div>
          
          <nav className="nav-links">
            <button onClick={() => showSection('home')} className={currentSection === 'home' ? 'active' : ''}>Accueil</button>
            <button onClick={() => showSection('prestataires')} className={currentSection === 'prestataires' ? 'active' : ''}>Prestataires</button>
            <button onClick={() => showSection('billetterie')} className={currentSection === 'billetterie' ? 'active' : ''}>Billetterie</button>
            <button onClick={() => showSection('mobilier')} className={currentSection === 'mobilier' ? 'active' : ''}>Mobilier</button>
            <button onClick={() => showSection('excursions')} className={currentSection === 'excursions' ? 'active' : ''}>Excursions</button>
            <button onClick={() => showSection('comptes')} className={currentSection === 'comptes' ? 'active' : ''}>Comptes</button>
            <button onClick={() => showSection('fidelite')} className={currentSection === 'fidelite' ? 'active' : ''}>Fidélité</button>
            <button onClick={() => showSection('pmr')} className={currentSection === 'pmr' ? 'active' : ''}>PMR</button>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        {/* Section Accueil */}
        {currentSection === 'home' && (
          <section className="section active">
            <div className="container">
              <h1>🏝️ Découvrez la Martinique</h1>
              <p>Villas de luxe et services exceptionnels dans un cadre paradisiaque</p>
              
              {/* Recherche fonctionnelle */}
              <div className="search-section">
                <h2>🔍 Rechercher une Villa</h2>
                <div className="booking-search-container">
                  <div className="search-field">
                    <label className="search-field-label">Destination</label>
                    <select 
                      value={searchFilters.destination} 
                      onChange={(e) => setSearchFilters(prev => ({...prev, destination: e.target.value}))}
                    >
                      <option value="">Toutes les destinations</option>
                      <option value="petit-macabou">Petit Macabou</option>
                      <option value="ste-anne">Sainte-Anne</option>
                      <option value="lamentin">Lamentin</option>
                      <option value="ste-luce">Sainte-Luce</option>
                      <option value="vauclin">Vauclin</option>
                      <option value="trinite">Trinité</option>
                      <option value="robert">Le Robert</option>
                      <option value="riviere-pilote">Rivière-Pilote</option>
                      <option value="ducos">Ducos</option>
                      <option value="fort-de-france">Fort-de-France</option>
                      <option value="trenelle">Trenelle</option>
                    </select>
                  </div>
                  
                  <div className="search-field">
                    <label className="search-field-label">Arrivée</label>
                    <input type="text" ref={checkinRef} placeholder="Sélectionner une date" />
                  </div>
                  
                  <div className="search-field">
                    <label className="search-field-label">Départ</label>
                    <input type="text" ref={checkoutRef} placeholder="Sélectionner une date" />
                  </div>
                  
                  <div className="search-field">
                    <label className="search-field-label">Voyageurs</label>
                    <select 
                      value={searchFilters.guests} 
                      onChange={(e) => setSearchFilters(prev => ({...prev, guests: e.target.value}))}
                    >
                      <option value="">Nombre de personnes</option>
                      <option value="2">2 personnes</option>
                      <option value="4">4 personnes</option>
                      <option value="6">6 personnes</option>
                      <option value="8">8 personnes</option>
                      <option value="10">10 personnes</option>
                      <option value="15">15+ personnes</option>
                    </select>
                  </div>
                  
                  <button className="search-button" onClick={performSearch}>
                    <i className="fas fa-search"></i>
                    Rechercher
                  </button>
                </div>
              </div>
              
              {/* Filtres */}
              <div className="filters">
                <button className={`filter-btn ${searchFilters.category === 'all' ? 'active' : ''}`} onClick={() => filterVillas('all')}>Toutes</button>
                <button className={`filter-btn ${searchFilters.category === 'sejour' ? 'active' : ''}`} onClick={() => filterVillas('sejour')}>Séjour</button>
                <button className={`filter-btn ${searchFilters.category === 'fete' ? 'active' : ''}`} onClick={() => filterVillas('fete')}>Fête/Journée</button>
                <button className={`filter-btn ${searchFilters.category === 'special' ? 'active' : ''}`} onClick={() => filterVillas('special')}>Spéciales</button>
              </div>
              
              <h2>🏖️ Nos 21 Villas de Luxe</h2>
              
              {/* Message de statut */}
              {statusMessage.text && (
                <div className={`status-message ${statusMessage.type}`}>
                  {statusMessage.text}
                </div>
              )}
              
              {/* Grille des villas */}
              <div className="villas-grid">
                {loading ? (
                  <div className="glass-card">
                    <h3>Chargement des villas...</h3>
                  </div>
                ) : filteredVillas.length === 0 ? (
                  <div className="glass-card">
                    <h3>Aucune villa trouvée</h3>
                    <p>Essayez de modifier vos critères de recherche.</p>
                  </div>
                ) : (
                  filteredVillas.map((villa) => (
                    <div key={villa.id} className="villa-card">
                      <div className="villa-image-container" style={{ height: '200px', overflow: 'hidden' }}>
                        <img 
                          src={`${process.env.REACT_APP_BACKEND_URL}${villa.image}`}
                          alt={villa.name}
                          className="villa-image"
                          onClick={() => openImageGallery(villa, 0)}
                          onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextElementSibling.style.display = 'flex';
                          }}
                          onLoad={(e) => {
                            e.target.nextElementSibling.style.display = 'none';
                          }}
                        />
                        <div className="image-placeholder" style={{ display: 'none' }} onClick={() => openImageGallery(villa, 0)}>
                          {villa.fallback_icon}
                        </div>
                      </div>
                      <div className="villa-content">
                        <h3>{villa.name}</h3>
                        <p><i className="fas fa-map-marker-alt"></i> {villa.location}</p>
                        <p><i className="fas fa-users"></i> {villa.guests_detail}</p>
                        <p><i className="fas fa-swimming-pool"></i> {villa.features}</p>
                        <div className="price">{villa.price}€/nuit</div>
                        <div className="villa-buttons">
                          <button className="btn-primary" onClick={() => openReservationModal(villa)}>Réserver</button>
                          <button className="btn-secondary" onClick={() => viewDetails(villa)}>Détails</button>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </section>
        )}

        {/* Section Prestataires */}
        {currentSection === 'prestataires' && (
          <section className="section active">
            <div className="container">
              <h1>🌊 Nos Prestataires de Services</h1>
              <p>Explorez nos services nautiques, culinaires et événementiels</p>
              
              <div className="villas-grid">
                <div className="glass-card">
                  <h3>🚤 Excursions Nautiques</h3>
                  <p>Découvrez la beauté de la Martinique depuis la mer avec nos excursions en catamaran.</p>
                  <div className="price">À partir de 120€/personne</div>
                  <button className="btn-primary" onClick={() => contactPrestataire('nautique')}>Réserver</button>
                </div>
                
                <div className="glass-card">
                  <h3>🍽️ Services Culinaires</h3>
                  <p>Savourez la cuisine créole authentique avec nos chefs professionnels.</p>
                  <div className="price">À partir de 80€/personne</div>
                  <button className="btn-primary" onClick={() => contactPrestataire('culinaire')}>Réserver</button>
                </div>
                
                <div className="glass-card">
                  <h3>🎉 Organisation d'Événements</h3>
                  <p>Confiez-nous l'organisation de vos événements mémorables.</p>
                  <div className="price">Devis personnalisé</div>
                  <button className="btn-primary" onClick={() => contactPrestataire('evenements')}>Demander un devis</button>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Autres sections */}
        {currentSection === 'billetterie' && (
          <section className="section active">
            <div className="container">
              <h1>🎫 Billetterie Événementielle</h1>
              <p>Organisez et participez aux meilleurs événements de Martinique</p>
              <div className="glass-card">
                <h3>🎭 Événements à Venir</h3>
                <p>Découvrez notre programmation d'événements culturels et festifs.</p>
                <button className="btn-primary" onClick={() => showComingSoon()}>Voir les événements</button>
              </div>
            </div>
          </section>
        )}

        {currentSection === 'mobilier' && (
          <section className="section active">
            <div className="container">
              <h1>🛋️ Location de Mobilier</h1>
              <p>Tables, chaises, décoration pour vos événements</p>
              <div className="glass-card">
                <h3>🪑 Mobilier d'Événement</h3>
                <p>Location de mobilier haut de gamme pour tous vos événements.</p>
                <button className="btn-primary" onClick={() => contactPrestataire('mobilier')}>Demander un devis</button>
              </div>
            </div>
          </section>
        )}

        {currentSection === 'excursions' && (
          <section className="section active">
            <div className="container">
              <h1>⛵ Excursions Inoubliables</h1>
              <p>Découvrez la Martinique par terre, mer et air</p>
              <div className="glass-card">
                <h3>🏝️ Tours de l'Île</h3>
                <p>Explorez les merveilles cachées de la Martinique avec nos guides experts.</p>
                <button className="btn-primary" onClick={() => contactPrestataire('excursions')}>Réserver</button>
              </div>
            </div>
          </section>
        )}

        {currentSection === 'comptes' && (
          <section className="section active">
            <div className="container">
              <h1>🐷 Comptes Vacances & Abonnements</h1>
              <p>Épargnez pour vos futures vacances avec nos comptes dédiés</p>
              <div className="glass-card">
                <h3>💰 Épargne Vacances</h3>
                <p>Constituez votre épargne pour des vacances de rêve en Martinique.</p>
                <button className="btn-primary" onClick={() => showComingSoon()}>En savoir plus</button>
              </div>
            </div>
          </section>
        )}

        {currentSection === 'fidelite' && (
          <section className="section active">
            <div className="container">
              <h1>🎁 Programme de Fidélité</h1>
              <p>Gagnez des points et des récompenses à chaque réservation</p>
              <div className="glass-card">
                <h3>⭐ Rewards Club</h3>
                <p>Rejoignez notre programme de fidélité et bénéficiez d'avantages exclusifs.</p>
                <button className="btn-primary" onClick={() => showComingSoon()}>Rejoindre</button>
              </div>
            </div>
          </section>
        )}

        {currentSection === 'pmr' && (
          <section className="section active">
            <div className="container">
              <h1>👑 Accessibilité PMR</h1>
              <p>Des séjours adaptés pour tous</p>
              <div className="glass-card">
                <h3>♿ Villas Accessibles</h3>
                <p>Découvrez nos villas spécialement aménagées pour les personnes à mobilité réduite.</p>
                <button className="btn-primary" onClick={() => filterVillas('pmr')}>Voir les villas PMR</button>
              </div>
            </div>
          </section>
        )}
      </main>

      {/* Page de détail d'une villa */}
      {showVillaDetail && selectedVilla && (
        <div className="villa-detail-page">
          <div className="villa-detail-container">
            {/* Header de la fiche villa */}
            <div className="villa-detail-header">
              <button className="back-button" onClick={closeVillaDetail}>
                <i className="fas fa-arrow-left"></i>
                <span>Retour aux villas</span>
              </button>
              
              <div className="villa-title-section">
                <h1 className="villa-detail-title">
                  🏖️ {selectedVilla.name}
                </h1>
                
                {/* Badges informatifs */}
                <div className="villa-badges">
                  <span className="villa-badge primary">
                    <i className="fas fa-map-marker-alt"></i>
                    {selectedVilla.location.includes('mer') || selectedVilla.location.includes('Anne') || 
                     selectedVilla.location.includes('Macabou') ? 'Villa Mer' : 'Villa Terre'}
                  </span>
                  <span className="villa-badge">
                    <i className="fas fa-users"></i>
                    {selectedVilla.guests} personnes
                  </span>
                  <span className="villa-badge">
                    <i className="fas fa-bed"></i>
                    {selectedVilla.name.includes('F5') ? '5' : 
                     selectedVilla.name.includes('F3') ? '3' : 
                     selectedVilla.name.includes('Studio') ? '1' : '3'} chambres
                  </span>
                  {selectedVilla.features.includes('Piscine') && (
                    <span className="villa-badge">
                      <i className="fas fa-swimming-pool"></i>
                      Piscine privée
                    </span>
                  )}
                  <span className="villa-badge location">
                    <i className="fas fa-map-pin"></i>
                    {selectedVilla.location.split(',')[0] || selectedVilla.location}
                  </span>
                </div>
              </div>
            </div>

            <div className="villa-detail-content">
              {/* Image principale et galerie */}
              <div className="villa-detail-media">
                <div className="main-image-container">
                  <img 
                    src={`${process.env.REACT_APP_BACKEND_URL}${selectedVilla.image}`}
                    alt={selectedVilla.name}
                    className="villa-main-image"
                    onClick={() => openImageGallery(selectedVilla, 0)}
                  />
                </div>
                
                {/* Galerie miniatures */}
                <div className="villa-thumbnails">
                  {selectedVilla.gallery && selectedVilla.gallery.slice(0, 6).map((image, index) => (
                    <img 
                      key={index}
                      src={`${process.env.REACT_APP_BACKEND_URL}${image}`}
                      alt={`${selectedVilla.name} - Image ${index + 1}`}
                      className="villa-thumbnail"
                      onClick={() => openImageGallery(selectedVilla, index)}
                    />
                  ))}
                </div>
              </div>

              {/* Informations et tarifs */}
              <div className="villa-detail-info">
                {/* Section Caractéristiques */}
                <div className="villa-characteristics">
                  <h3>
                    <i className="fas fa-home"></i>
                    Caractéristiques
                  </h3>
                  
                  <div className="characteristic-item">
                    <i className="fas fa-expand-arrows-alt"></i>
                    <span>Surface :</span>
                    <span>
                      {selectedVilla.name.includes('F5') ? '250m²' : 
                       selectedVilla.name.includes('F3') ? '150m²' : 
                       selectedVilla.name.includes('Studio') ? '45m²' : '180m²'}
                    </span>
                  </div>
                  
                  <div className="characteristic-item">
                    <i className="fas fa-bed"></i>
                    <span>Chambres :</span>
                    <span>
                      {selectedVilla.name.includes('F5') ? '5 (avec clim)' : 
                       selectedVilla.name.includes('F3') ? '3 (avec clim)' : 
                       selectedVilla.name.includes('Studio') ? '1 (avec clim)' : '3 (avec clim)'}
                    </span>
                  </div>
                  
                  <div className="characteristic-item">
                    <i className="fas fa-bath"></i>
                    <span>Salles de bain :</span>
                    <span>
                      {selectedVilla.name.includes('F5') ? '3' : 
                       selectedVilla.name.includes('F3') ? '2' : 
                       selectedVilla.name.includes('Studio') ? '1' : '2'}
                    </span>
                  </div>
                  
                  {selectedVilla.features.includes('Piscine') && (
                    <div className="characteristic-item">
                      <i className="fas fa-swimming-pool"></i>
                      <span>Piscine privée :</span>
                      <span>8x4m</span>
                    </div>
                  )}
                  
                  <div className="characteristic-item">
                    <i className="fas fa-users"></i>
                    <span>Capacité :</span>
                    <span>{selectedVilla.guests_detail}</span>
                  </div>
                </div>

                {/* Section Tarifs */}
                <div className="villa-pricing">
                  <h3>
                    <i className="fas fa-euro-sign"></i>
                    Tarifs
                  </h3>
                  
                  <div className="price-main">
                    <span className="price-amount">{selectedVilla.price}€</span>
                    <span className="price-unit">/ nuit</span>
                  </div>
                  
                  <div className="price-info">
                    <small>Tarif basse saison</small>
                  </div>
                  
                  <button 
                    className="btn-reserve-detail"
                    onClick={() => openReservationFromDetail(selectedVilla)}
                  >
                    <i className="fas fa-calendar-check"></i>
                    Réserver maintenant
                  </button>
                </div>

                {/* Section Description */}
                <div className="villa-description">
                  <h3>
                    <i className="fas fa-info-circle"></i>
                    À propos de cette villa
                  </h3>
                  <p>{selectedVilla.description}</p>
                  
                  <h4>Équipements inclus :</h4>
                  <div className="amenities-list">
                    {selectedVilla.amenities && selectedVilla.amenities.map((amenity, index) => (
                      <span key={index} className="amenity-tag">
                        <i className={
                          amenity.includes('Piscine') ? 'fas fa-swimming-pool' :
                          amenity.includes('WiFi') ? 'fas fa-wifi' :
                          amenity.includes('Cuisine') ? 'fas fa-utensils' :
                          amenity.includes('Climatisation') ? 'fas fa-snowflake' :
                          amenity.includes('Sauna') ? 'fas fa-hot-tub' :
                          amenity.includes('Jacuzzi') ? 'fas fa-spa' :
                          amenity.includes('Vue') ? 'fas fa-eye' :
                          amenity.includes('Terrasse') ? 'fas fa-building' :
                          amenity.includes('Jardin') ? 'fas fa-seedling' :
                          amenity.includes('Parking') ? 'fas fa-parking' :
                          'fas fa-check'
                        }></i>
                        {amenity}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal de réservation */}
      {showReservationModal && (
        <div className="modal active">
          <div className="modal-content">
            <span className="close" onClick={closeReservationModal}>&times;</span>
            <h2>Réservation - {currentVilla?.name}</h2>
            
            <form onSubmit={handleReservationSubmit}>
              <div className="form-group">
                <label htmlFor="customerName">Nom complet *</label>
                <input 
                  type="text" 
                  id="customerName" 
                  value={reservationData.customerName}
                  onChange={(e) => setReservationData(prev => ({...prev, customerName: e.target.value}))}
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="customerEmail">Email *</label>
                <input 
                  type="email" 
                  id="customerEmail" 
                  value={reservationData.customerEmail}
                  onChange={(e) => setReservationData(prev => ({...prev, customerEmail: e.target.value}))}
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="customerPhone">Téléphone *</label>
                <input 
                  type="tel" 
                  id="customerPhone" 
                  value={reservationData.customerPhone}
                  onChange={(e) => setReservationData(prev => ({...prev, customerPhone: e.target.value}))}
                  required 
                />
              </div>
              
              <div style={{ display: 'flex', gap: '1rem' }}>
                <div className="form-group" style={{ flex: 1 }}>
                  <label htmlFor="modalCheckin">Date d'arrivée *</label>
                  <input type="text" ref={modalCheckinRef} required />
                </div>
                
                <div className="form-group" style={{ flex: 1 }}>
                  <label htmlFor="modalCheckout">Date de départ *</label>
                  <input type="text" ref={modalCheckoutRef} required />
                </div>
              </div>
              
              <div className="form-group">
                <label htmlFor="modalGuests">Nombre de voyageurs *</label>
                <select 
                  id="modalGuests" 
                  value={reservationData.guestsCount}
                  onChange={(e) => setReservationData(prev => ({...prev, guestsCount: e.target.value}))}
                  required
                >
                  <option value="">Choisir le nombre</option>
                  <option value="2">2 personnes</option>
                  <option value="4">4 personnes</option>
                  <option value="6">6 personnes</option>
                  <option value="8">8 personnes</option>
                  <option value="10">10 personnes</option>
                  <option value="15">15+ personnes</option>
                </select>
              </div>
              
              {reservationData.checkinDate && reservationData.checkoutDate && (
                <div className="price-summary">
                  <h3>📋 Résumé de la réservation</h3>
                  <div className="price-line">
                    <span>Villa :</span>
                    <span>{currentVilla?.name}</span>
                  </div>
                  <div className="price-line">
                    <span>Dates :</span>
                    <span>{reservationData.checkinDate} - {reservationData.checkoutDate}</span>
                  </div>
                  <div className="price-line">
                    <span>Prix par nuit :</span>
                    <span>{currentVilla?.price}€</span>
                  </div>
                  <div className="price-line price-total">
                    <span>Total :</span>
                    <span>{calculateTotalPrice()}€</span>
                  </div>
                </div>
              )}
              
              <div className="form-group">
                <label htmlFor="customerMessage">Message ou demandes spéciales</label>
                <textarea 
                  id="customerMessage" 
                  rows="3" 
                  placeholder="Décrivez vos besoins particuliers..."
                  value={reservationData.message}
                  onChange={(e) => setReservationData(prev => ({...prev, message: e.target.value}))}
                />
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
                <button type="button" onClick={closeReservationModal} className="btn-secondary" style={{ flex: 1 }}>Annuler</button>
                <button type="submit" className="btn-primary" style={{ flex: 2 }}>
                  <i className="fas fa-calendar-check"></i>
                  Confirmer la réservation
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal de galerie d'images */}
      {showGalleryModal && (
        <div className="image-gallery-modal active">
          <div className="gallery-content">
            <span className="gallery-close" onClick={closeImageGallery}>&times;</span>
            <button className="gallery-nav gallery-prev" onClick={previousImage}>❮</button>
            <img 
              src={`${process.env.REACT_APP_BACKEND_URL}${currentGallery[currentGalleryIndex]}`} 
              className="gallery-image" 
              alt="" 
            />
            <button className="gallery-nav gallery-next" onClick={nextImage}>❯</button>
            
            <div className="gallery-thumbnails">
              {currentGallery.map((image, index) => (
                <img 
                  key={index}
                  src={`${process.env.REACT_APP_BACKEND_URL}${image}`} 
                  className={`thumbnail ${index === currentGalleryIndex ? 'active' : ''}`} 
                  onClick={() => goToImage(index)}
                  alt=""
                />
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;