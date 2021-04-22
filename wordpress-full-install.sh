#!/bin/sh

# Update/Upgrade système

apt-get update && apt-get upgrade -y

# SSH/firewall

ufw allow OpenSSH
ufw --force enable

# Installion Apache

apt-get install apache2 -y

# Modification du firewall pour apache

ufw allow 'Apache Full'

# Installion et sécurisation MySQL

apt-get install mysql-server -y
mysql_secure_installation

# mysql/firewall

ufw allow mysql

# Start mysqlserver

systemctl start mysql
systemctl enable mysql

# Création d une database wordpress, dun user MySQL wordpressuser et contrôle total sur la base de données wordpress à l'utilisateur wordpressuser

echo
echo "Saisir le mot de passe root sql"
echo
mysql -u root -p -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'password'; CREATE DATABASE wordpress character set utf8; CREATE USER 'wordpressuser'@'%' IDENTIFIED WITH mysql_native_password BY 'password'; GRANT ALL ON wordpress.* TO 'wordpressuser'@'%'; FLUSH PRIVILEGES";

# Installation phpmyadmin

apt-get install phpmyadmin php-mbstring php-zip php-gd php-json php-curl -y
wget https://files.phpmyadmin.net/phpMyAdmin/5.0.2/phpMyAdmin-5.0.2-all-languages.zip
apt-get install unzip -y
unzip phpMyAdmin-5.0.2-all-languages.zip
mv phpMyAdmin-5.0.2-all-languages /usr/share/phpmyadmin
mkdir /usr/share/phpmyadmin/tmp
chown -R www-data:www-data /usr/share/phpmyadmin
chmod 777 /usr/share/phpmyadmin/tmp
cp files/apache2.conf /etc/apache2/apache2.conf

# Redémarrage apache

systemctl restart apache2

# Supression du fichier phpMyAdmin-5.0.2-all-languages.zip

rm phpMyAdmin-5.0.2-all-languages.zip

# Module à installer

apt-get install php-curl php-gd php-mbstring php-xml php-xmlrpc php-soap php-intl php-zip -y

# Activation module a2enmod

a2enmod rewrite

# Redémarrage apache

systemctl restart apache2

# Copie du fichier wordpress.conf dans /etc/apache2/sites-available/ pour créer un hôte virtuel

cp files/wordpress.conf /etc/apache2/sites-available/

# Activation de l'hôte virtuel
 
sudo a2ensite wordpress

# Rechargement apache

systemctl reload apache2

# Téléchargement de la dernière version de WordPress

wget https://wordpress.org/latest.tar.gz

# Décompression de l'archive wordpress-latest-fr_FR.zip

tar -zxvf latest.tar.gz
mv wordpress /var/www/
rm latest.tar.gz

# Attribution de droits restrictifs aux fichiers suivants

chown -R www-data:www-data /var/www/wordpress 
chmod -R -wx,u+rwX,g+rX,o+rX /var/www/wordpress
find /var/www/wordpress/ -type d -exec chmod 750 {} \;
find /var/www/wordpress/ -type f -exec chmod 640 {} \;
cp files/wp-config.php /var/www/wordpress/wp-config.php
cp files/000-default.conf /etc/apache2/sites-available/000-default.conf

# Restart apache2

service apache2 restart

# Confirmation de la fin d'installation

clear
echo "L'installation de wordpress est terminée."
echo

# Configuration du nom d hôte, changement IP en 10.0.0.7 et reboot

echo "La machine server va redémarrer dans 10 secondes"
sleep 10
cp files/00-installer-config.yaml /etc/netplan/00-installer-config.yaml
cp files/hostname /etc/hostname
cp files/hosts /etc/hosts
netplan apply
systemctl restart systemd-networkd
reboot
