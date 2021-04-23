#!/bin/sh

# Nettoyage de l'écran

clear

# Installation de Nagios Plugins et NRPE Server

apt-get install nagios-nrpe-server monitoring-plugins -y

# Copie du fichier de configuration nrpe.cfg

cp files/nrpe.cfg /etc/nagios/nrpe.cfg

# Redémarrage du service NRPE et activation au démarrage système

systemctl restart nagios-nrpe-server
systemctl enable nagios-nrpe-server

# Nettoyage de l écran et confirmation de l installation du monitoring

clear
echo "Le monitoring Nagios est bien installé."
