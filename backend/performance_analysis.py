"""
Analyse des Performances KhanelConcept API
========================================

Script pour analyser les résultats des tests de charge
et générer des recommandations d'optimisation.

Usage:
    python performance_analysis.py [fichier_log_k6.json]
"""

import json
import sys
import statistics
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {}
        self.recommendations = []
        
    def analyze_k6_results(self, log_file=None):
        """Analyser les résultats k6"""
        if log_file and Path(log_file).exists():
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                self._parse_k6_data(data)
            except Exception as e:
                print(f"❌ Erreur lecture fichier k6: {e}")
        else:
            print("⚠️  Fichier de résultats k6 non trouvé")
            
    def analyze_locust_results(self, html_file=None):
        """Analyser les résultats Locust HTML"""
        # Pour une analyse complète, il faudrait parser le HTML
        # ou utiliser les CSV générés par Locust
        print("📊 Analyse Locust disponible dans l'interface web")
        
    def simulate_typical_results(self):
        """Simuler des résultats typiques pour démonstration"""
        print("📊 Simulation de résultats typiques...")
        
        # Résultats simulés basés sur une API FastAPI optimisée
        self.metrics = {
            'total_requests': 15420,
            'failed_requests': 78,
            'success_rate': 99.49,
            'avg_response_time': 145.2,
            'p50_response_time': 98.5,
            'p95_response_time': 387.2,
            'p99_response_time': 892.1,
            'max_response_time': 1456.8,
            'rps': 51.4,
            'concurrent_users': 100,
            'test_duration': 300,
            'endpoints': {
                '/api/health': {
                    'requests': 1540,
                    'avg_time': 45.2,
                    'success_rate': 100.0
                },
                '/api/villas': {
                    'requests': 3080,
                    'avg_time': 125.8,
                    'success_rate': 99.8
                },
                '/api/villas/search': {
                    'requests': 4620,
                    'avg_time': 168.4,
                    'success_rate': 99.2
                },
                '/api/reservations': {
                    'requests': 1540,
                    'avg_time': 234.7,
                    'success_rate': 98.9
                },
                '/api/admin/login': {
                    'requests': 462,
                    'avg_time': 89.3,
                    'success_rate': 99.6
                },
                '/api/stats/dashboard': {
                    'requests': 1540,
                    'avg_time': 78.9,
                    'success_rate': 99.9
                }
            }
        }
        
    def evaluate_performance(self):
        """Évaluer les performances et générer des recommandations"""
        print("\n🎯 ANALYSE DES PERFORMANCES")
        print("=" * 50)
        
        # Évaluation globale
        success_rate = self.metrics.get('success_rate', 0)
        avg_response = self.metrics.get('avg_response_time', 0)
        p95_response = self.metrics.get('p95_response_time', 0)
        
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        if success_rate >= 99:
            print("   ✅ EXCELLENT - Très peu d'erreurs")
        elif success_rate >= 95:
            print("   ✅ BON - Taux d'erreur acceptable")  
        elif success_rate >= 90:
            print("   ⚠️  MOYEN - Quelques problèmes à résoudre")
        else:
            print("   ❌ FAIBLE - Problèmes critiques")
            self.recommendations.append("🔧 Investiguer les erreurs serveur fréquentes")
            
        print(f"⏱️  Temps de réponse moyen: {avg_response:.1f}ms")
        if avg_response <= 100:
            print("   ✅ EXCELLENT - Très rapide")
        elif avg_response <= 300:
            print("   ✅ BON - Performance acceptable")
        elif avg_response <= 1000:
            print("   ⚠️  MOYEN - Optimisations possibles")
        else:
            print("   ❌ LENT - Optimisations nécessaires")
            self.recommendations.append("🚀 Optimiser les requêtes lentes")
            
        print(f"📊 P95 (95e percentile): {p95_response:.1f}ms")
        if p95_response <= 500:
            print("   ✅ EXCELLENT - Latence faible même en pic")
        elif p95_response <= 2000:
            print("   ✅ BON - Latence gérable")
        else:
            print("   ⚠️  ÉLEVÉ - Attention aux pics de charge")
            self.recommendations.append("📈 Optimiser la gestion des pics de charge")
            
        # Analyse par endpoint
        print(f"\n🎯 ANALYSE PAR ENDPOINT")
        print("-" * 30)
        
        endpoints = self.metrics.get('endpoints', {})
        for endpoint, stats in endpoints.items():
            avg_time = stats.get('avg_time', 0)
            success_rate = stats.get('success_rate', 0)
            requests = stats.get('requests', 0)
            
            status = "✅" if success_rate > 98 and avg_time < 200 else "⚠️" if success_rate > 95 else "❌"
            print(f"{status} {endpoint}")
            print(f"   Requêtes: {requests} | Temps: {avg_time:.1f}ms | Succès: {success_rate:.1f}%")
            
            # Recommandations spécifiques
            if endpoint == '/api/villas/search' and avg_time > 150:
                self.recommendations.append("🔍 Optimiser l'index de recherche des villas")
            elif endpoint == '/api/reservations' and avg_time > 200:
                self.recommendations.append("📝 Optimiser la création de réservations")
                
    def generate_recommendations(self):
        """Générer des recommandations d'optimisation"""
        print(f"\n💡 RECOMMANDATIONS D'OPTIMISATION")
        print("=" * 40)
        
        # Recommandations générales
        base_recommendations = [
            "🗃️  Implémenter un cache Redis pour les villas fréquemment consultées",
            "📊 Ajouter des index MongoDB sur les champs de recherche",
            "🔄 Optimiser les requêtes avec des projections spécifiques",
            "📈 Implémenter une pagination pour les grandes listes",
            "🛡️  Ajouter un rate limiting plus granulaire par utilisateur",
            "📝 Optimiser la sérialisation JSON avec orjson",
            "🚀 Considérer FastAPI avec uvloop pour plus de performance",
            "📦 Configurer la compression gzip pour les réponses",
            "🔒 Utiliser des connexions persistantes pour MongoDB"
        ]
        
        # Ajouter les recommandations spécifiques
        all_recommendations = list(set(self.recommendations + base_recommendations))
        
        for i, rec in enumerate(all_recommendations, 1):
            print(f"{i:2d}. {rec}")
            
        # Priorités
        print(f"\n⭐ PRIORITÉS HAUTES:")
        high_priority = [
            "Optimiser les requêtes les plus lentes",
            "Implémenter le cache pour les données fréquentes", 
            "Ajouter des index sur les champs de recherche"
        ]
        
        for i, priority in enumerate(high_priority, 1):
            print(f"   {i}. {priority}")
            
    def generate_report(self):
        """Générer un rapport complet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"performance_report_{timestamp}.md"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 📊 Rapport de Performance - KhanelConcept API\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Durée du test:** {self.metrics.get('test_duration', 'N/A')}s\n")
            f.write(f"**Utilisateurs simultanés:** {self.metrics.get('concurrent_users', 'N/A')}\n\n")
            
            f.write("## 📈 Métriques Globales\n\n")
            f.write(f"- **Requêtes totales:** {self.metrics.get('total_requests', 'N/A'):,}\n")
            f.write(f"- **Taux de réussite:** {self.metrics.get('success_rate', 'N/A'):.1f}%\n")
            f.write(f"- **RPS moyen:** {self.metrics.get('rps', 'N/A'):.1f} req/sec\n")
            f.write(f"- **Temps de réponse moyen:** {self.metrics.get('avg_response_time', 'N/A'):.1f}ms\n")
            f.write(f"- **P95:** {self.metrics.get('p95_response_time', 'N/A'):.1f}ms\n\n")
            
            f.write("## 🎯 Performance par Endpoint\n\n")
            endpoints = self.metrics.get('endpoints', {})
            for endpoint, stats in endpoints.items():
                f.write(f"### {endpoint}\n")
                f.write(f"- Requêtes: {stats.get('requests', 0):,}\n")
                f.write(f"- Temps moyen: {stats.get('avg_time', 0):.1f}ms\n") 
                f.write(f"- Taux de succès: {stats.get('success_rate', 0):.1f}%\n\n")
                
            f.write("## 💡 Recommandations\n\n")
            for i, rec in enumerate(self.recommendations, 1):
                f.write(f"{i}. {rec}\n")
                
        print(f"\n📄 Rapport généré: {report_file}")
        
    def create_charts(self):
        """Créer des graphiques de performance"""
        try:
            import matplotlib.pyplot as plt
            
            # Graphique des temps de réponse par endpoint
            endpoints = self.metrics.get('endpoints', {})
            if endpoints:
                names = list(endpoints.keys())
                times = [stats.get('avg_time', 0) for stats in endpoints.values()]
                
                plt.figure(figsize=(12, 6))
                plt.bar(range(len(names)), times)
                plt.xlabel('Endpoints')
                plt.ylabel('Temps de réponse (ms)')
                plt.title('Temps de réponse moyen par endpoint')
                plt.xticks(range(len(names)), [name.split('/')[-1] for name in names], rotation=45)
                plt.tight_layout()
                
                chart_file = f"performance_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(chart_file, dpi=150, bbox_inches='tight')
                print(f"📊 Graphique généré: {chart_file}")
                plt.close()
                
        except ImportError:
            print("📊 Matplotlib non installé - graphiques ignorés")
            print("💡 Installation: pip install matplotlib")

def main():
    """Fonction principale"""
    analyzer = PerformanceAnalyzer()
    
    print("🔍 ANALYSEUR DE PERFORMANCE - KhanelConcept API")
    print("=" * 50)
    
    # Vérifier si un fichier de résultats est fourni
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
        print(f"📁 Analyse du fichier: {log_file}")
        analyzer.analyze_k6_results(log_file)
    else:
        print("📊 Aucun fichier fourni - utilisation de données simulées")
        analyzer.simulate_typical_results()
    
    # Effectuer l'analyse
    analyzer.evaluate_performance()
    analyzer.generate_recommendations()
    analyzer.generate_report()
    analyzer.create_charts()
    
    print(f"\n🎉 Analyse terminée!")
    print("💡 Consultez le rapport généré pour plus de détails")

if __name__ == "__main__":
    main()