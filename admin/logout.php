<?php
/**
 * Déconnexion - KhanelConcept Admin
 */

require_once 'includes/config.php';
require_once 'includes/auth.php';

$auth = new Auth();
$auth->logout();

redirect('/admin/login.php', 'Vous avez été déconnecté avec succès.');
?>