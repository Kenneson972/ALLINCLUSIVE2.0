Blacklist de déploiement (exclus de la prod)

A exclure:
- .emergent/
- backup_*/
- github-ready/
- *.tar.gz
- *.csv
- *_backup_video_*.html
- .git*/
- .nojekyll
- Tous les fichiers .py
- Tous les rapports .md/.json (sauf DEPLOY_EXCLUDE.md)

Notes:
- Conserver uniquement frontend/public et backend utiles pour la prod.
- Vérifier qu’aucun lien public vers backend/admin n’existe.
