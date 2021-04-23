#!/bin/sh

# Nettoyage de l'ecran

clear

# Création du dossier crontab /root/crontab

mkdir crontab
mv crontab /root
# Création des dossiers scripts et logs dans /root/crontab

mkdir scripts
mv scripts /root/crontab
mkdir logs
mv logs /root/crontab

# Copier le fichier crontab dans /var/spool/cron/crontabs pour créer la tache de sauvegarde wordpress

cp -r files/backupwordressonly/ /root/crontab/scripts/
cp files/root /var/spool/cron/crontabs/

# Redémarrer crontab

systemctl restart cron

# Nettoyage de l'écran

clear

# Confirmation de la création de la tache

echo "La tâche d'exécution de la sauvegarde quotidienne du site wordpress a bien été créée dans crontab"
