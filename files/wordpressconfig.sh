#!/bin/sh

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

# Attribution de droits restrictifs aux fichiers suivants

chown -R www-data:www-data /var/www/wordpress 
chmod -R -wx,u+rwX,g+rX,o+rX /var/www/wordpress
find /var/www/wordpress/ -type d -exec chmod 750 {} \;
find /var/www/wordpress/ -type f -exec chmod 640 {} \;
cp files/000-default.conf /etc/apache2/sites-available/000-default.conf

# Restart apache2

service apache2 restart
