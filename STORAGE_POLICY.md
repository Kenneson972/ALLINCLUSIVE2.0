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
