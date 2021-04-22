![Python 3.6](https://img.shields.io/badge/python-3.6%2B-green)
![MIT](https://img.shields.io/badge/license-MIT-green)

# Backup-Restore-Wordpress

Ce Script python permet d' installer/restaurer/sauvegarder en intégralité un site Wordpress depuis/vers un SFTP. 

## Pour commencer

WordPress est un logiciel destiné à la conception et à la mise à jour dynamique de sites web ou d'applications multimédias. L'objectif de ce script est de pouvoir sauvegarder et restaurer un site wordpress complet en un minimum de temps.

### Pré-requis

Le script ne fonctionnera que sur un système disposant d'un serveur LAMP (Linux, Apache, MySQL, PHP) et d'une installation Wordpress.

Environnement lors de la fabrication du script :

- Ubuntu Server 20.04
- Apache 2
- MySQL 8.0.23
- PHP 7.4.3
- Wordpress 5.7
- Python 3.8.5

### Installation et configuration

1) Installer le paquet python3 sur votre système d'exploitation linux si celui-ci ne le possède pas déjà. Pour un Ubuntu Server 20.04, saisir la commande suivante dans un terminal:
```shell
sudo apt-get update -y && apt-get upgrade -y && apt-get install python3 -y
```
2) Installer le gestionnaire de paquet python pip. Pour Ubuntu Server 20.04, saisir la commande suivante dans un terminal:
```shell
sudo apt-get install python3-pip -y
```
4) Télécharger le contenu du dépôt https://github.com/Jewlse/Backup-Restore-Wordpress dans un dossier en local sur votre machine.

5) Installer les modules python3 listés dans le fichier requirements.txt, ils sont indispensables à la bonne exécution du script. Pour un Ubuntu Server 20.04, saisir la commande suivante dans un terminal:
```shell
sudo pip3 install -r requirements.txt
```
Cette commande doit être exécutée dans le dossier contenant le fichier requirements.txt.

6) Ouvrir le fichier myconfiguration.py avec un editeur de texte et saisir les informations propres à votre installation à la place des XXXXXXXXXXX.

## Démarrage

Lancer le script en saissisant la commande suivante dans un terminal qui pointe vers le dossier dans lequel se trouve le contenu du dépôt https://github.com/Jewlse/Backup-Restore-Wordpress

```shell
sudo python3 install-backup-restore-wordpress.py
```

## Version du script

* Version 1.0.0 : 
    * Mise à disposition du script sur Github le 14/04/21

## Auteurs
* **Julien Dirr** _alias_ [@Jewlse](https://github.com/Jewlse)

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](https://github.com/Jewlse/Backup-Restore-Wordpress/blob/main/LICENSE) pour plus d'informations



