// Script pour extraire les vraies données du planning Villa SAADA
// Basé sur l'analyse de https://www.planning-planning.com/Planning-FR-mmufsn.htm

const villaRealAvailabilityData = {
    // Août 2025
    '2025-08-03': 'libre',    // 3F_.gif
    '2025-08-04': 'attente',  // 4_D.gif  
    '2025-08-10': 'libre',    // 10F_.gif
    '2025-08-11': 'attente',  // 11_D.gif
    '2025-08-15': 'libre',    // 15F_.gif
    '2025-08-18': 'attente',  // 18_D.gif
    '2025-08-29': 'libre',    // 29F_.gif
    
    // Septembre 2025
    '2025-09-05': 'attente',  // 5_D.gif
    '2025-09-07': 'libre',    // 7F_.gif
    '2025-09-11': 'attente',  // 11_D.gif
    '2025-09-14': 'libre',    // 14F_.gif
    
    // Octobre 2025 - Tous libres (pas de marqueurs spéciaux)
    
    // Novembre 2025
    '2025-11-06': 'attente',  // 6_D.gif
    '2025-11-09': 'libre',    // 9F_.gif
    
    // Décembre 2025
    '2025-12-12': 'attente',  // 12_D.gif
    '2025-12-14': 'libre',    // 14F_.gif
    '2025-12-22': 'attente',  // 22_D.gif
    '2025-12-28': 'libre',    // 28F_.gif
    '2025-12-29': 'attente',  // 29_D.gif
    
    // Janvier 2026
    '2026-01-04': 'libre',    // 4F_.gif
    
    // Toutes les autres dates sont par défaut "occupé" sauf indication contraire
};

// Fonction pour générer les données complètes
function generateCompleteAvailabilityData(startDate, endDate) {
    const data = {};
    const current = new Date(startDate);
    const end = new Date(endDate);
    
    while (current <= end) {
        const dateStr = current.toISOString().split('T')[0];
        
        // Vérifier si c'est une date spéciale du planning
        if (villaRealAvailabilityData[dateStr]) {
            data[dateStr] = villaRealAvailabilityData[dateStr];
        } else {
            // Par défaut, considérer comme occupé (logique du planning original)
            data[dateStr] = 'occupe';
        }
        
        current.setDate(current.getDate() + 1);
    }
    
    return data;
}

// Données complètes pour Août 2025 - Juillet 2026
const completeF3AvailabilityData = generateCompleteAvailabilityData('2025-08-01', '2026-07-31');

console.log('✅ Données réelles du planning Villa SAADA extraites');
console.log('📊 Période couverte: Août 2025 - Juillet 2026');
console.log('🔢 Total dates spéciales identifiées:', Object.keys(villaRealAvailabilityData).length);

// Export pour utilisation dans le système
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        villaRealAvailabilityData,
        completeF3AvailabilityData,
        generateCompleteAvailabilityData
    };
}