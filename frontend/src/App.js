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
  const [currentView, setCurrentView] = useState('home'); // 'home' ou 'villa'
  const [selectedVilla, setSelectedVilla] = useState(null);
  const [selectedSeason, setSelectedSeason] = useState('basse'); // 'basse' ou 'haute'
  
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
  
  // États pour l'autocomplete de localisation
  const [showLocationSuggestions, setShowLocationSuggestions] = useState(false);
  const [locationSuggestions, setLocationSuggestions] = useState([]);
  
  // États pour le dropdown voyageurs
  const [showVoyageursDropdown, setShowVoyageursDropdown] = useState(false);
  const [voyageursCount, setVoyageursCount] = useState({
    adultes: 2,
    enfants: 0,
    bebes: 0
  });
  
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

  const handleCategoryFilter = (category) => {
    filterVillas(category);
  };

  // Liste des communes de Martinique pour l'autocomplete
  const communesMartinique = [
    'Sainte-Anne', 'Vauclin', 'Lamentin', 'Macabou', 'Sainte-Luce', 
    'Trinité', 'Le Robert', 'Rivière-Pilote', 'Ducos', 'Fort-de-France', 
    'Trenelle', 'Le Marin', 'Rivière-Salée', 'Les Trois-Îlets', 
    'Le Diamant', 'Les Anses-d\'Arlet', 'Le Carbet', 'Bellefontaine',
    'Case-Pilote', 'Schoelcher', 'Saint-Joseph', 'Le Lorrain',
    'Marigot', 'Sainte-Marie', 'Le Prêcheur', 'Grand\'Rivière',
    'L\'Ajoupa-Bouillon', 'Basse-Pointe', 'Macouba', 'Le Morne-Rouge',
    'Saint-Pierre', 'Le Morne-Vert', 'Fonds-Saint-Denis'
  ];

  // Fonction pour gérer l'input de localisation
  const handleLocationInput = (e) => {
    const value = e.target.value;
    setSearchFilters(prev => ({ ...prev, destination: value }));
    
    if (value.length > 0) {
      const filtered = communesMartinique.filter(commune =>
        commune.toLowerCase().includes(value.toLowerCase())
      );
      setLocationSuggestions(filtered.slice(0, 5));
    } else {
      setLocationSuggestions([]);
    }
  };

  // Fonction pour sélectionner une localisation
  const selectLocation = (commune) => {
    setSearchFilters(prev => ({ ...prev, destination: commune }));
    setLocationSuggestions([]);
    setShowLocationSuggestions(false);
  };

  // Fonction pour toggle le dropdown voyageurs
  const toggleVoyageursDropdown = () => {
    setShowVoyageursDropdown(!showVoyageursDropdown);
  };

  // Fonction pour mettre à jour le nombre de voyageurs
  const updateVoyageurs = (type, increment) => {
    setVoyageursCount(prev => ({
      ...prev,
      [type]: Math.max(0, prev[type] + increment)
    }));
  };

  // Fonction pour afficher le texte des voyageurs
  const getVoyageursDisplay = () => {
    const total = voyageursCount.adultes + voyageursCount.enfants + voyageursCount.bebes;
    if (total === 0) return 'Ajouter des voyageurs';
    
    let display = `${voyageursCount.adultes} adulte${voyageursCount.adultes > 1 ? 's' : ''}`;
    if (voyageursCount.enfants > 0) {
      display += `, ${voyageursCount.enfants} enfant${voyageursCount.enfants > 1 ? 's' : ''}`;
    }
    if (voyageursCount.bebes > 0) {
      display += `, ${voyageursCount.bebes} bébé${voyageursCount.bebes > 1 ? 's' : ''}`;
    }
    
    return display;
  };

  // Gestion des clics en dehors des dropdowns
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showLocationSuggestions && !event.target.closest('.location-field')) {
        setShowLocationSuggestions(false);
      }
      if (showVoyageursDropdown && !event.target.closest('.voyageurs-field')) {
        setShowVoyageursDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showLocationSuggestions, showVoyageursDropdown]);

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

  // Fonction pour gérer les filtres de catégorie (alias pour filterVillas)
  const handleCategoryFilter = (category) => {
    filterVillas(category);
  };

  // Liste des communes de Martinique pour l'autocomplete
  const communesMartinique = [
    'Sainte-Anne', 'Vauclin', 'Lamentin', 'Macabou', 'Sainte-Luce', 
    'Trinité', 'Le Robert', 'Rivière-Pilote', 'Ducos', 'Fort-de-France', 
    'Trenelle', 'Le Marin', 'Rivière-Salée', 'Les Trois-Îlets', 
    'Le Diamant', 'Les Anses-d\'Arlet', 'Le Carbet', 'Bellefontaine',
    'Case-Pilote', 'Schoelcher', 'Saint-Joseph', 'Le Lorrain',
    'Marigot', 'Sainte-Marie', 'Le Prêcheur', 'Grand\'Rivière',
    'L\'Ajoupa-Bouillon', 'Basse-Pointe', 'Macouba', 'Le Morne-Rouge',
    'Saint-Pierre', 'Le Morne-Vert', 'Fonds-Saint-Denis'
  ];

  // Fonction pour gérer l'input de localisation
  const handleLocationInput = (e) => {
    const value = e.target.value;
    setSearchFilters(prev => ({ ...prev, destination: value }));
    
    if (value.length > 0) {
      const filtered = communesMartinique.filter(commune =>
        commune.toLowerCase().includes(value.toLowerCase())
      );
      setLocationSuggestions(filtered.slice(0, 5)); // Limiter à 5 suggestions
    } else {
      setLocationSuggestions([]);
    }
  };

  // Fonction pour sélectionner une localisation
  const selectLocation = (commune) => {
    setSearchFilters(prev => ({ ...prev, destination: commune }));
    setLocationSuggestions([]);
    setShowLocationSuggestions(false);
  };

  // Fonction pour toggle le dropdown voyageurs
  const toggleVoyageursDropdown = () => {
    setShowVoyageursDropdown(!showVoyageursDropdown);
  };

  // Fonction pour mettre à jour le nombre de voyageurs
  const updateVoyageurs = (type, increment) => {
    setVoyageursCount(prev => ({
      ...prev,
      [type]: Math.max(0, prev[type] + increment)
    }));
  };

  // Fonction pour afficher le texte des voyageurs
  const getVoyageursDisplay = () => {
    const total = voyageursCount.adultes + voyageursCount.enfants + voyageursCount.bebes;
    if (total === 0) return 'Ajouter des voyageurs';
    
    let display = `${voyageursCount.adultes} adulte${voyageursCount.adultes > 1 ? 's' : ''}`;
    if (voyageursCount.enfants > 0) {
      display += `, ${voyageursCount.enfants} enfant${voyageursCount.enfants > 1 ? 's' : ''}`;
    }
    if (voyageursCount.bebes > 0) {
      display += `, ${voyageursCount.bebes} bébé${voyageursCount.bebes > 1 ? 's' : ''}`;
    }
    
    return display;
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
    setCurrentView('villa');
    // Mettre à jour l'URL du navigateur
    window.history.pushState({}, '', `/villa/${villa.id}`);
  };

  const closeVillaDetail = () => {
    setCurrentView('home');
    setSelectedVilla(null);
    setSelectedSeason('basse');
    // Retourner à l'URL principale
    window.history.pushState({}, '', '/');
  };

  const toggleSeason = (season) => {
    setSelectedSeason(season);
  };

  const getCurrentPrice = () => {
    if (!selectedVilla) return 0;
    // Augmenter de 30% en haute saison
    return selectedSeason === 'haute' 
      ? Math.round(selectedVilla.price * 1.3) 
      : selectedVilla.price;
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

  // Gestion des clics en dehors des dropdowns
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (showLocationSuggestions && !event.target.closest('.location-field')) {
        setShowLocationSuggestions(false);
      }
      if (showVoyageursDropdown && !event.target.closest('.voyageurs-field')) {
        setShowVoyageursDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [showLocationSuggestions, showVoyageursDropdown]);

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
      
      if (currentView === 'villa') {
        if (e.key === 'Escape') closeVillaDetail();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [showGalleryModal, showReservationModal, currentView, currentGallery.length]);

  return (
    <div className="App">
      {/* Fond vidéo Cloudinary */}
      <div className="video-background-loop">
        <video
          className="background-video"
          autoPlay
          muted
          loop
          playsInline
        >
          <source
            src="https://res.cloudinary.com/ddulasmtz/video/upload/v1752950782/background-video.mp4_qoofsz.mp4"
            type="video/mp4"
          />
          Votre navigateur ne supporte pas les vidéos HTML5.
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
              <div className="search-container">
                <h2 className="search-title">🔍 Rechercher une Villa</h2>
                
                <div className="villa-search-form">
                  {/* Localisation avec autocomplete - Position 1 */}
                  <div className="search-field location-field">
                    <label htmlFor="location-search">📍 Localisation</label>
                    <input 
                      type="text" 
                      id="location-search" 
                      className="location-input"
                      placeholder="Tapez une ville..."
                      autoComplete="off"
                      value={searchFilters.destination}
                      onChange={handleLocationInput}
                      onFocus={() => setShowLocationSuggestions(true)}
                    />
                    {showLocationSuggestions && locationSuggestions.length > 0 && (
                      <div className="location-suggestions" id="suggestions-dropdown">
                        {locationSuggestions.map((commune, index) => (
                          <div 
                            key={index}
                            className="suggestion-item"
                            onClick={() => selectLocation(commune)}
                          >
                            📍 {commune}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  {/* Date d'arrivée - Position 2 */}
                  <div className="search-field">
                    <label htmlFor="checkin">ARRIVÉE</label>
                    <input type="text" id="checkin" ref={checkinRef} placeholder="Sélectionner une date" />
                  </div>
                  
                  {/* Date de départ - Position 3 */}
                  <div className="search-field">
                    <label htmlFor="checkout">DÉPART</label>
                    <input type="text" id="checkout" ref={checkoutRef} placeholder="Sélectionner une date" />
                  </div>
                  
                  {/* Bouton rechercher - Position 4 */}
                  <div className="search-field">
                    <button className="search-btn" onClick={performSearch}>
                      <i className="fas fa-search"></i>
                      Rechercher
                    </button>
                  </div>
                  
                  {/* Voyageurs - POSITIONNÉ EN BAS À DROITE - Position 5 */}
                  <div className="search-field voyageurs-field bottom-right-position">
                    <label>👥 Voyageurs</label>
                    <div className="voyageurs-dropdown">
                      <input 
                        type="text" 
                        className="voyageurs-display" 
                        value={getVoyageursDisplay()}
                        readOnly
                        onClick={toggleVoyageursDropdown}
                      />
                      
                      {showVoyageursDropdown && (
                        <div className="dropdown-menu voyageurs-menu">
                          {/* Adultes */}
                          <div className="voyageur-row">
                            <div className="voyageur-info">
                              <span className="voyageur-label">Adultes</span>
                              <small>13 ans et plus</small>
                            </div>
                            <div className="voyageur-counter">
                              <button 
                                type="button" 
                                className="counter-btn minus" 
                                onClick={() => updateVoyageurs('adultes', -1)}
                                disabled={voyageursCount.adultes <= 1}
                              >-</button>
                              <span className="counter-value">{voyageursCount.adultes}</span>
                              <button 
                                type="button" 
                                className="counter-btn plus" 
                                onClick={() => updateVoyageurs('adultes', 1)}
                              >+</button>
                            </div>
                          </div>
                          
                          {/* Enfants */}
                          <div className="voyageur-row">
                            <div className="voyageur-info">
                              <span className="voyageur-label">Enfants</span>
                              <small>2-12 ans</small>
                            </div>
                            <div className="voyageur-counter">
                              <button 
                                type="button" 
                                className="counter-btn minus" 
                                onClick={() => updateVoyageurs('enfants', -1)}
                                disabled={voyageursCount.enfants <= 0}
                              >-</button>
                              <span className="counter-value">{voyageursCount.enfants}</span>
                              <button 
                                type="button" 
                                className="counter-btn plus" 
                                onClick={() => updateVoyageurs('enfants', 1)}
                              >+</button>
                            </div>
                          </div>
                          
                          {/* Bébés */}
                          <div className="voyageur-row">
                            <div className="voyageur-info">
                              <span className="voyageur-label">Bébés</span>
                              <small>0-2 ans</small>
                            </div>
                            <div className="voyageur-counter">
                              <button 
                                type="button" 
                                className="counter-btn minus" 
                                onClick={() => updateVoyageurs('bebes', -1)}
                                disabled={voyageursCount.bebes <= 0}
                              >-</button>
                              <span className="counter-value">{voyageursCount.bebes}</span>
                              <button 
                                type="button" 
                                className="counter-btn plus" 
                                onClick={() => updateVoyageurs('bebes', 1)}
                              >+</button>
                            </div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
                
                <div className="category-filters">
                  <button 
                    className={searchFilters.category === 'all' ? 'active' : ''}
                    onClick={() => handleCategoryFilter('all')}
                  >
                    Toutes
                  </button>
                  <button 
                    className={searchFilters.category === 'sejour' ? 'active' : ''}
                    onClick={() => handleCategoryFilter('sejour')}
                  >
                    Séjour
                  </button>
                  <button 
                    className={searchFilters.category === 'fete' ? 'active' : ''}
                    onClick={() => handleCategoryFilter('fete')}
                  >
                    Fête/Journée
                  </button>
                  <button 
                    className={searchFilters.category === 'speciales' ? 'active' : ''}
                    onClick={() => handleCategoryFilter('speciales')}
                  >
                    Spéciales
                  </button>
                </div>
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

      {/* Page Villa Dédiée - Remplace le Modal */}
      {currentView === 'villa' && selectedVilla && (
        <div className="villa-page">
          {/* Header de la page villa */}
          <div className="villa-page-header">
            <button className="villa-back-button" onClick={closeVillaDetail}>
              <i className="fas fa-arrow-left"></i>
              Retour aux villas
            </button>
            <div className="villa-page-logo">
              <h1>KhanelConcept</h1>
            </div>
          </div>

          <div className="villa-page-content">
            {/* Hero Section */}
            <div className="villa-page-hero">
              <h1 className="villa-hero-title">
                🏖️ {selectedVilla.name}
              </h1>
              <p className="villa-hero-location">
                <i className="fas fa-map-marker-alt"></i> {selectedVilla.location}
              </p>
              <button 
                className="villa-hero-cta"
                onClick={() => openReservationFromDetail(selectedVilla)}
              >
                <i className="fas fa-calendar-check"></i> Réserver maintenant
              </button>
            </div>

            {/* Grid Caractéristiques Tropicales */}
            <div className="villa-characteristics-grid">
              <div className="villa-characteristic-card">
                <span className="villa-card-icon">🏊‍♀️</span>
                <h3 className="villa-card-title">Piscine</h3>
                <p className="villa-card-value">
                  {selectedVilla.features.includes('Piscine') || selectedVilla.amenities.includes('Piscine') ? '8x4m privée' : 'Non disponible'}
                </p>
              </div>
              
              <div className="villa-characteristic-card">
                <span className="villa-card-icon">🛏️</span>
                <h3 className="villa-card-title">Chambres</h3>
                <p className="villa-card-value">
                  {selectedVilla.name.includes('F5') ? '5 chambres' : 
                   selectedVilla.name.includes('F3') ? '3 chambres' : 
                   selectedVilla.name.includes('Studio') ? '1 chambre' : '3 chambres'}
                </p>
              </div>
              
              <div className="villa-characteristic-card">
                <span className="villa-card-icon">🚿</span>
                <h3 className="villa-card-title">Salles de bain</h3>
                <p className="villa-card-value">
                  {selectedVilla.name.includes('F5') ? '3 SDB' : 
                   selectedVilla.name.includes('F3') ? '2 SDB' : 
                   selectedVilla.name.includes('Studio') ? '1 SDB' : '2 SDB'}
                </p>
              </div>
              
              <div className="villa-characteristic-card">
                <span className="villa-card-icon">🌊</span>
                <h3 className="villa-card-title">Terrasse</h3>
                <p className="villa-card-value">
                  {selectedVilla.name.includes('F5') ? '120m²' : 
                   selectedVilla.name.includes('F3') ? '80m²' : 
                   selectedVilla.name.includes('Studio') ? '25m²' : '80m²'} vue mer
                </p>
              </div>
            </div>

            {/* Section Tarifs avec Toggle */}
            <div className="villa-pricing-section">
              <div className="villa-pricing-header">
                <h3 className="villa-pricing-title">
                  <i className="fas fa-euro-sign"></i> Tarifs
                </h3>
                <div className="villa-season-toggle">
                  <button 
                    className={`villa-season-button ${selectedSeason === 'basse' ? 'active' : ''}`}
                    onClick={() => toggleSeason('basse')}
                  >
                    Basse saison
                  </button>
                  <button 
                    className={`villa-season-button ${selectedSeason === 'haute' ? 'active' : ''}`}
                    onClick={() => toggleSeason('haute')}
                  >
                    Haute saison
                  </button>
                </div>
              </div>
              
              <div className="villa-price-display">
                <span className="villa-price-amount">{getCurrentPrice()}€</span>
                <span className="villa-price-unit">/ nuit</span>
              </div>
              
              <p style={{ color: 'rgba(255, 255, 255, 0.7)', fontSize: '14px', fontFamily: 'Inter' }}>
                {selectedSeason === 'basse' 
                  ? 'Septembre - Novembre & Janvier - Mars' 
                  : 'Décembre & Avril - Août (+30%)'}
              </p>
            </div>

            {/* Description Immersive */}
            <div className="villa-description-section">
              <h3 className="villa-description-title">
                <i className="fas fa-info-circle"></i> Description luxe tropical
              </h3>
              <p className="villa-description-text">
                {selectedVilla.description || `Découvrez cette magnifique villa ${selectedVilla.name} située à ${selectedVilla.location}. 
                Un véritable havre de paix tropical où le luxe rencontre l'authenticité caribéenne. 
                Profitez d'un cadre exceptionnel avec toutes les commodités modernes pour des vacances inoubliables en Martinique.`}
              </p>
              
              <h4 className="villa-description-title" style={{ fontSize: '20px', marginBottom: '16px' }}>
                🏝️ Équipements tropicaux
              </h4>
              
              <div className="villa-amenities-grid">
                {selectedVilla.amenities && selectedVilla.amenities.map((amenity, index) => (
                  <div key={index} className="villa-amenity-item">
                    <i className={`villa-amenity-icon ${
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
                    }`}></i>
                    <span className="villa-amenity-text">{amenity}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Section Localisation */}
            <div className="villa-location-section">
              <h3 className="villa-location-title">
                <i className="fas fa-map-marker-alt"></i> Localisation & Distances
              </h3>
              
              <ul className="villa-location-list">
                <li className="villa-location-item">
                  <i className="villa-location-icon fas fa-umbrella-beach"></i>
                  <span className="villa-location-text">
                    {selectedVilla.location.includes('Sainte-Anne') || selectedVilla.location.includes('Ste Anne') 
                      ? 'Plage des Salines - 2km' 
                      : selectedVilla.location.includes('Macabou') 
                      ? 'Plage de Macabou - 1km'
                      : selectedVilla.location.includes('Lamentin')
                      ? 'Centre commercial - 5km'
                      : 'Plages paradisiaques - 3km'}
                  </span>
                </li>
                <li className="villa-location-item">
                  <i className="villa-location-icon fas fa-plane"></i>
                  <span className="villa-location-text">Aéroport Martinique - 45min</span>
                </li>
                <li className="villa-location-item">
                  <i className="villa-location-icon fas fa-shopping-cart"></i>
                  <span className="villa-location-text">Supermarché le plus proche - 10min</span>
                </li>
                <li className="villa-location-item">
                  <i className="villa-location-icon fas fa-utensils"></i>
                  <span className="villa-location-text">Restaurants créoles - 15min</span>
                </li>
                <li className="villa-location-item">
                  <i className="villa-location-icon fas fa-sailboat"></i>
                  <span className="villa-location-text">Marina & excursions - 20min</span>
                </li>
              </ul>
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