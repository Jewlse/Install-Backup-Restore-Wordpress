#!/bin/sh

# Nettoyage de l'ecran

clear

# Création du dossier crontab /root/crontab

mkdir crontab

# Création des dossiers scripts et logs dans /root/crontab

mkdir /root/crontab/scripts
mkdir /root/crontab/logs

# Copier le fichier crontab dans /var/spool/cron/crontabs pour créer la tache de sauvegarde wordpress

cp file/backupwordpressonly /root/crontab/scripts/backupwordpressonly
cp file/root /var/spool/cron/crontabs/root

# Redémarrer crontab

systemctl restart cron

# Nettoyage de l'écran

Clear

# Confirmation de la création de la tache

echo "La tâche d'exécution de la sauvegarde quotidienne du site wordpress a bien été créée dans crontab"
