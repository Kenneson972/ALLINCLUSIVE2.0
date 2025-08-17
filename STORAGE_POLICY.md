# Storage Policy — KhanelConcept

Whitelist autorisée (TTL):
- kc:consent — 365 jours
- kc:ui:lang — 365 jours
- kc:ui:theme — 365 jours
- kc:cache:* — 24 heures

Blocages/remplacements:
- Toutes les écritures hors kc:* sont bloquées (console.warn). Les modules métiers (villas, réservations, settings, images, sync) n'utilisent plus localStorage.

Purge:
- Ajouter ?purge_storage=1 à l'URL purge toutes les clés kc:* et affiche un bandeau "Stockage local purgé".

Implémentation:
- Wrapper kcStorage (assets/js/storage-guard.js) avec TTL et suppression automatique des entrées expirées.
- Intégré avant les autres scripts via <script src="assets/js/storage-guard.js"></script> dans index.html et villas.html.

Portée: Sitewide
- storage-guard.js est chargé sur toutes les pages publiques, avant config.js, puis le reste des scripts UI.
- Purge disponible partout via ?purge_storage=1

Ordre de chargement garanti:
1) assets/js/storage-guard.js
2) assets/js/config.js
3) autres scripts UI

Vérification:
- Un scan automatique a injecté le script manquant et corrigé l'ordre si nécessaire.
