Liquid Glass Patch (Apple-like 1:1)

1) Charger le patch en dernier (idéal):
   &lt;link rel="stylesheet" href="/assets/css/liquid-glass.patch.css"&gt;

   Si vous ne voulez pas toucher l'HTML, vous pouvez copier/coller le contenu
   de liquid-glass.patch.css à la fin de chaque fichier CSS listé.

2) Réfraction: insérer le snippet SVG juste avant </body>
   Voir /assets/liquid-glass-refract-snippet.html

3) Où ajouter les utilitaires:
   - Sur éléments premium (en-tête, hero card, modals clés): ajouter classe lg-edge (dans HTML quand possible).
   - Pour effet "liquide" plus fort localement: ajouter classe lg-refract (nécessite le SVG).

4) Réglages mobiles (si lag iOS):
   :root{ --lg-blur: 20px; --lg-noise-opacity: 0; }
   @media (prefers-reduced-motion: reduce){ animations sheen coupées }