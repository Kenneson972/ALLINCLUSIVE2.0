#!/usr/bin/env python3
"""
Mise à jour de l'index.html pour pointer vers les 21 nouvelles pages villa
"""

import re

def update_index_navigation():
    """Met à jour les liens de navigation dans index.html"""
    
    # Nouveau mapping des villas vers les pages
    villa_mapping = {
        'villa-f3-petit-macabou': 'villa-villa-f3-sur-petit-macabou.html',
        'villa-f3-baccha': 'villa-villa-f3-pour-la-baccha.html', 
        'villa-f3-francois': 'villa-villa-f3-sur-le-franois.html',
        'villa-f5-ste-anne': 'villa-villa-f5-sur-ste-anne.html',
        'villa-f6-lamentin': 'villa-villa-f6-au-lamentin.html',
        'villa-f6-ste-luce': 'villa-villa-f6-sur-ste-luce-a-1mn-de-la-plage.html',
        'villa-f3-trinite': 'villa-villa-f3-bas-de-villa-trinite-cosmy.html',
        'villa-f3-robert': 'villa-bas-de-villa-f3-sur-le-robert.html',
        'villa-f3-trenelle': 'villa-appartement-f3-trenelle-location-annuelle.html',
        'villa-f5-vauclin': 'villa-villa-f5-vauclin-ravine-plate.html',
        'villa-f5-la-renee': 'villa-villa-f5-la-renee.html',
        'villa-f7-baie-mulets': 'villa-villa-f7-baie-des-mulets.html',
        'villa-f3-ste-luce': 'villa-bas-de-villa-f3-sur-ste-luce.html',
        'villa-studio-lamentin': 'villa-studio-cocooning-lamentin.html',
        'villa-fete-ducos': 'villa-villa-fte-journee-ducos.html',
        'villa-fete-fort-de-france': 'villa-villa-fte-journee-fort-de-france.html',
        'villa-fete-riviere-pilote': 'villa-villa-fte-journee-riviere-pilote.html',
        'villa-fete-riviere-salee': 'villa-villa-fte-journee-riviere-salee.html',
        'villa-fete-sainte-luce': 'villa-villa-fte-journee-sainte-luce.html',
        'villa-espace-piscine': 'villa-espace-piscine-journee-bungalow.html',
        'villa-f6-petit-macabou-fete': 'villa-villa-f6-sur-petit-macabou-sejour--fte.html'
    }
    
    try:
        # Lire l'index.html actuel
        with open('/app/index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("📝 Mise à jour des liens de navigation dans index.html...")
        
        # Chercher et remplacer la fonction viewDetails
        pattern = r'function viewDetails\(villaId\) \{[^}]*\}'
        
        new_view_details = '''function viewDetails(villaId) {
            console.log('🏠 Navigation vers villa:', villaId);
            
            // Mapping des IDs vers les nouvelles pages
            const villaPages = {
                'villa-f3-petit-macabou': 'villa-villa-f3-sur-petit-macabou.html',
                'villa-f3-baccha': 'villa-villa-f3-pour-la-baccha.html', 
                'villa-f3-francois': 'villa-villa-f3-sur-le-franois.html',
                'villa-f5-ste-anne': 'villa-villa-f5-sur-ste-anne.html',
                'villa-f6-lamentin': 'villa-villa-f6-au-lamentin.html',
                'villa-f6-ste-luce': 'villa-villa-f6-sur-ste-luce-a-1mn-de-la-plage.html',
                'villa-f3-trinite': 'villa-villa-f3-bas-de-villa-trinite-cosmy.html',
                'villa-f3-robert': 'villa-bas-de-villa-f3-sur-le-robert.html',
                'villa-f3-trenelle': 'villa-appartement-f3-trenelle-location-annuelle.html',
                'villa-f5-vauclin': 'villa-villa-f5-vauclin-ravine-plate.html',
                'villa-f5-la-renee': 'villa-villa-f5-la-renee.html',
                'villa-f7-baie-mulets': 'villa-villa-f7-baie-des-mulets.html',
                'villa-f3-ste-luce': 'villa-bas-de-villa-f3-sur-ste-luce.html',
                'villa-studio-lamentin': 'villa-studio-cocooning-lamentin.html',
                'villa-fete-ducos': 'villa-villa-fte-journee-ducos.html',
                'villa-fete-fort-de-france': 'villa-villa-fte-journee-fort-de-france.html',
                'villa-fete-riviere-pilote': 'villa-villa-fte-journee-riviere-pilote.html',
                'villa-fete-riviere-salee': 'villa-villa-fte-journee-riviere-salee.html',
                'villa-fete-sainte-luce': 'villa-villa-fte-journee-sainte-luce.html',
                'villa-espace-piscine': 'villa-espace-piscine-journee-bungalow.html',
                'villa-f6-petit-macabou-fete': 'villa-villa-f6-sur-petit-macabou-sejour--fte.html'
            };
            
            const targetPage = villaPages[villaId];
            if (targetPage) {
                console.log('✅ Redirection vers:', targetPage);
                window.location.href = './' + targetPage;
            } else {
                console.log('❌ Villa non trouvée:', villaId);
                alert('Villa non trouvée: ' + villaId);
            }
        }'''
        
        # Remplacer la fonction
        content = re.sub(pattern, new_view_details, content, flags=re.DOTALL)
        
        # Écrire le fichier mis à jour
        with open('/app/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Index.html mis à jour avec les nouveaux liens villa !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")
        return False

def main():
    print("🔗 MISE À JOUR NAVIGATION INDEX.HTML")
    print("Redirection vers les 21 nouvelles pages villa")
    print("=" * 50)
    
    success = update_index_navigation()
    
    if success:
        print("\n✅ TERMINÉ: Index.html pointe maintenant vers les 21 vraies pages villa !")
        print("🏠 Navigation opérationnelle depuis l'accueil")
    else:
        print("\n❌ ÉCHEC: Problème lors de la mise à jour")

if __name__ == "__main__":
    main()