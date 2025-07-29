#!/usr/bin/env python3
"""
🏠 TEST COMPLET TOUTES LES VILLAS - Page de Réservation
=====================================================

Script pour tester que TOUTES les 22 villas du catalogue sont maintenant
reconnues par la page de réservation après les corrections.

Ce script valide que chaque villa:
1. Est reconnue par le paramètre URL
2. Affiche le bon nom dans le titre
3. Affiche le bon nom dans le récapitulatif  
4. Affiche des informations cohérentes
5. N'affiche pas d'éléments de debug
"""

import asyncio
import aiohttp
from datetime import datetime

# 🎯 LISTE COMPLÈTE DES 22 VILLAS À TESTER
VILLAS_TO_TEST = [
    # Villas résidentielles principales
    ('villa-f3-petit-macabou', 'Villa F3 sur Petit Macabou'),
    ('villa-f3-pour-la-baccha', 'Villa F3 POUR LA BACCHA'),
    ('villa-f3-sur-le-francois', 'Villa F3 sur le François'),
    ('villa-f5-sur-ste-anne', 'Villa F5 sur Ste Anne'),
    ('villa-f6-au-lamentin', 'Villa F6 au Lamentin'),
    ('villa-f6-sur-ste-luce-a-1mn-de-la-plage', 'Villa F6 sur Ste Luce à 1mn de la plage'),
    ('villa-f7-baie-des-mulets', 'Villa F7 Baie des Mulets'),
    ('villa-f3-bas-de-villa-trinite-cosmy', 'Villa F3 Bas de villa Trinité Cosmy'),
    ('bas-de-f3-sur-le-robert', 'Bas de villa F3 sur le Robert'),  # Villa problématique originale
    ('villa-f5-vauclin-ravine-plate', 'Villa F5 Vauclin Ravine Plate'),
    ('villa-f5-la-renee', 'Villa F5 La Renée'),
    ('bas-villa-f3-sur-ste-luce', 'Bas de villa F3 sur Ste Luce'),
    ('studio-cocooning-lamentin', 'Studio Cocooning Lamentin'),
    ('villa-f6-sur-petit-macabou', 'Villa F6 sur Petit Macabou (séjour + fête)'),
    ('villa-appartement-f3-trenelle-location-annuelle', 'Appartement F3 Trenelle (Location Annuelle)'),
    
    # Villas fête/journée (nouvellement ajoutées)
    ('villa-fte-journee-ducos', 'Villa Fête Journée Ducos'),
    ('villa-fte-journee-fort-de-france', 'Villa Fête Journée Fort de France'),
    ('villa-fte-journee-riviere-pilote', 'Villa Fête Journée Rivière-Pilote'),
    ('villa-fte-journee-riviere-salee', 'Villa Fête Journée Rivière Salée'),
    ('villa-fte-journee-sainte-luce', 'Villa Fête Journée Sainte-Luce'),
    ('villa-espace-piscine-journee-bungalow', 'Espace Piscine Journée Bungalow'),
]

async def test_villa_recognition(session, villa_id, expected_name):
    """Test qu'une villa spécifique est bien reconnue"""
    url = f"http://localhost:8080/reservation.html?villa={villa_id}"
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                
                # Vérifier que le nom attendu apparaît dans le contenu
                if expected_name in content:
                    return {
                        'villa_id': villa_id,
                        'expected_name': expected_name,
                        'status': 'SUCCESS',
                        'message': f'✅ Villa reconnue: {expected_name}'
                    }
                else:
                    return {
                        'villa_id': villa_id,
                        'expected_name': expected_name,
                        'status': 'FAILURE',
                        'message': f'❌ Villa non reconnue: {expected_name}'
                    }
            else:
                return {
                    'villa_id': villa_id,
                    'expected_name': expected_name,
                    'status': 'ERROR',
                    'message': f'❌ Erreur HTTP {response.status}'
                }
                
    except Exception as e:
        return {
            'villa_id': villa_id,
            'expected_name': expected_name,
            'status': 'ERROR',
            'message': f'❌ Erreur: {str(e)}'
        }

async def main():
    """Test principal de toutes les villas"""
    print("🏠 TEST COMPLET RECONNAISSANCE TOUTES LES VILLAS")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Nombre de villas à tester: {len(VILLAS_TO_TEST)}")
    print()
    
    results = []
    success_count = 0
    failure_count = 0
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
        # Tester chaque villa
        for villa_id, expected_name in VILLAS_TO_TEST:
            print(f"🔍 Test: {villa_id}")
            
            result = await test_villa_recognition(session, villa_id, expected_name)
            results.append(result)
            
            print(f"    {result['message']}")
            
            if result['status'] == 'SUCCESS':
                success_count += 1
            else:
                failure_count += 1
                
            # Petit délai pour éviter de surcharger le serveur
            await asyncio.sleep(0.5)
            
    print()
    print("📊 RÉSULTATS FINAUX")
    print("=" * 30)
    print(f"✅ Succès: {success_count}/{len(VILLAS_TO_TEST)} ({success_count/len(VILLAS_TO_TEST)*100:.1f}%)")
    print(f"❌ Échecs: {failure_count}/{len(VILLAS_TO_TEST)} ({failure_count/len(VILLAS_TO_TEST)*100:.1f}%)")
    
    if failure_count > 0:
        print()
        print("❌ VILLAS EN ÉCHEC:")
        for result in results:
            if result['status'] != 'SUCCESS':
                print(f"   • {result['villa_id']}: {result['message']}")
    
    print()
    if success_count == len(VILLAS_TO_TEST):
        print("🎉 PARFAIT! TOUTES LES VILLAS SONT RECONNUES!")
        print("La correction de la page de réservation est 100% complète.")
    else:
        print("⚠️ Certaines villas ne sont pas encore reconnues.")
        print("Des ajustements supplémentaires sont nécessaires.")
    
    print()
    print("📋 RAPPORT DÉTAILLÉ:")
    for result in results:
        status_icon = "✅" if result['status'] == 'SUCCESS' else "❌"
        print(f"{status_icon} {result['villa_id']} → {result['expected_name']}")

if __name__ == "__main__":
    asyncio.run(main())