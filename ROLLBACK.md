# Rollback — Front statique

1) Sauvegarder l'état actuel du site (o2switch cPanel → gestionnaire de fichiers → compresser public_html)
2) Restaurer l'archive connue (rollback_front_now.zip) en remplaçant le contenu de public_html
3) Désactiver HSTS si activé (cPanel → Domaine → Security/HSTS) pour éviter cache strict
4) Vider caches (navigateur/CDN) et recharger
5) En cas de sous-domaine, repointer DNS vers l'ancienne instance si besoin
