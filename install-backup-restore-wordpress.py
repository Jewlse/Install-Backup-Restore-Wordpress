#!/usr/bin/env python

import os
import tarfile
import datetime
import time
import paramiko
import subprocess
from myconfiguration import *

os.system("clear")

### Fonction de sauvegarde de wordpress vers le SFTP

def backupwordpresstosftp():

    # Arret du service apache

    os.system("systemctl stop apache2.service")

    # Execution du backup de la base de données wordpress et copie du backup à la racine /root

    os.system("clear")
    command = "mysqldump -u " + mysqluser +" --password=" + mysqlpassword + " wordpress > /root/backupmysql.sql"
    os.system(command)
    os.system("clear")
    print("Sauvegarde de la base de données Wordpress et du dossier " + wordpresslocalpath + " en cours, veuillez patienter.")

    # Mise en variable du fichier /root/backupwordpress.tar.gz

    file_name_wp = "/root/backupwordpress.tar.gz"

    # Archivage du dossier wordpress pour le backup wordpress

    tar = tarfile.open(file_name_wp, "w:gz")
    os.chdir(wordpresslocalpath)
    for name in os.listdir("."):
        tar.add(name)
    tar.close()

    # Redemarrage du service apache

    os.system("systemctl start apache2.service")

    # Connection ssh_client

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password, port=port)

    # Depot des fichiers backupmysql et backupwordpress sur le SFTP avec renommage à la date du jour

    datestamp = datetime.datetime.now()
    antislash = ('/')
    backupmysql = 'backupmysql.sql'
    backupwordpress = 'backupwordpress.tar.gz'
    backupmysqlwithdate = "backupmysql.sql."+(datestamp.strftime("%d%m%y"))
    backupwordpresswithdate = "backupwordpress.tar.gz."+(datestamp.strftime("%d%m%y"))
    backupmysqlwithdate_path = remotepath + antislash + backupmysql + '.'  + (datestamp.strftime("%d%m%y"))
    backupwordpresswithdate_path = remotepath + antislash + backupwordpress + '.'  + (datestamp.strftime("%d%m%y"))
    remote_backupmysql = remotepath + antislash + backupmysql
    remote_backupwordpress = remotepath + antislash + backupwordpress

    ftp_client = ssh_client.open_sftp()
    print()
    print("Chargement du fichier", backupmysqlwithdate,"sur le SFTP.")
    ftp_client.put('/root/backupmysql.sql', backupmysqlwithdate_path)
    print()
    print("Chargement du fichier", backupwordpresswithdate,"sur le SFTP.")
    ftp_client.put('/root/backupwordpress.tar.gz', backupwordpresswithdate_path)
    ftp_client.close()

    # Suppression des fichiers qui ont dépassé la durée de stockage renseignée dans le fichier myconfiguration

    transport = paramiko.Transport((host, port))
    transport.connect(username = username, password = password)

    sftp = paramiko.SFTPClient.from_transport(transport)

    for entry in sftp.listdir_attr(remotepath):
        timestamp = entry.st_mtime
        createtime = datetime.datetime.fromtimestamp(timestamp)
        now = datetime.datetime.now()
        delta = now - createtime
        if delta > datetime.timedelta(minutes=storageduration):
            filepath = remotepath + '/' + entry.filename
            sftp.remove(filepath)
    sftp.close()
    transport.close()

    # Suppression des fichiers backupmysql.tar.gz et backupwordpress.tar.gz dans /root local

    os.system("rm /root/backupmysql.sql")
    os.system("rm /root/backupwordpress.tar.gz")
    os.system("clear")

    # Confirmation de la bonne exécution de la sauvegarde

    print("La sauvegarde de Wordpress sur le SFTP s'est bien déroulée.")

### Fonction de restauration de wordpress depuis le SFTP

def restorewordpressfromsftp():

    # Connection ssh_client

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password, port=port)

    # Liste les fichiers dans le dossier backupwebsite et les affiches

    sftp = ssh_client.open_sftp()
    files = sftp.listdir(remotepath)
    os.system("clear")
    print ("Voici la liste des backupwordpress et backupmysql actuellement disponibles sur le SFTP:")
    print ()
    print (files)
    print ()
    ssh_client.close()

    # Choix et telechargements des backupwordpress et backupmysql du SFTP vers le répertoire local /root

    backupmysql = (input("Saisir le nom du fichier backupmysql à restaurer : "))
    backupwordpress = (input("Saisir le nom du fichier backupwordpress à restaurer : "))
    print()
    print("Téléchargement des fichiers en cours, veuillez patienter.")
    print()
    antislash = ('/')
    remote_backupmysql = remotepath + antislash + backupmysql
    remote_backupwordpress = remotepath + antislash + backupwordpress

    os.system("mkdir /root/backup")
    localpathmysql = "/root/backup/mysql.sql"
    localpathwordpress = "/root/backup/wordpress.tar.gz"

    try:
        ssh_client.connect(hostname=host, username=username, password=password, port=port)
        sftp = ssh_client.open_sftp()
        sftp.chdir(remotepath)
        try:
            print(sftp.stat(remote_backupmysql))
            sftp.get(remote_backupmysql,localpathmysql)
            print("Le fichier", backupmysql, "est présent sur le SFTP et a bien été téléchargé.")
        except IOError:
            os.system("clear")
            print("Le fichier", backupmysql, "n'est pas présent sur le SFTP, la restauration est annulée.")
            os.system("rm -r /root/backup")
            menu()
        ssh_client.close()
    except paramiko.SSHException:
        print("Connection Error")
        exit()

    try:
        ssh_client.connect(hostname=host, username=username, password=password, port=port)
        sftp = ssh_client.open_sftp()
        sftp.chdir(remotepath)
        try:
            print(sftp.stat(remote_backupwordpress))
            sftp.get(remote_backupwordpress,localpathwordpress)
            print("Le fichier", backupwordpress, "est présent sur le SFTP et a bien été téléchargé.")
        except IOError:
            os.system("clear")
            print("Le fichier", backupwordpress, "n'est pas présent sur le SFTP, la restauration est annulée.")
            os.system("rm -r /root/backup")
            menu()
        ssh_client.close()
    except paramiko.SSHException:
        print("Connection Error")
        exit()

    # Arret du service apache

    os.system("systemctl stop apache2.service")

    # Decompression de l'archive backupwordpress vers le dossier local wordpress

    tar = tarfile.open(localpathwordpress, "r:gz")
    tar.extractall(wordpresslocalpath)
    tar.close()

    # Restauration de la base de données wordpress dans MySQL

    os.system("clear")
    command = "mysql -u " + mysqluser +" --password=" + mysqlpassword + " --database=wordpress < /root/backup/mysql.sql"
    os.system(command)
    print("La restauration de la base de données Wordpress est en cours, veuillez patienter.")
    os.system("clear")

    # Demarrage du service apache

    os.system("systemctl start apache2.service")

    # Suppression des fichiers backupmysql.sql et backupwordpess.tar.gz dans /root local 

    os.system("rm -r /root/backup")
    os.system("clear")

    # Confirmation de la bonne exécution de la restauration

    print("La restauration de Wordpress depuis le SFTP s'est bien déroulée.")

### Fonction sortie du programme

def exitmenu():
    exit()

### Fonction affichage du menu

def menu():

    # Affichage du menu

    print("\nWordpress sur Ubuntu server 20.04 \n\n 1. Installation de Wordpress ( La machine redémarrera à la fin de l'installation ) \n 2. Sauvegarde de wordpress sur le SFTP \n 3. Restauration de wordpress depuis le SFTP \n 4. Installation du monitoring Nagios \n 5. Création d'une tache crontab pour la sauvegarde quotidienne du site wordpress \n 6. Sortir du menu \n")
    choice = input()

    if choice == "1":
        print()
        print("Installation de Wordpress ( La machine redémarrera à la fin de l'installation )\n")
        subprocess.call(['sh', './wordpress-full-install.sh'])
    if choice =="2":
        print("\nSauvegarde de Wordpress sur le SFTP.")
        backupwordpresstosftp()
        menu()
    if choice =="3":
        print("\nRestauration de la sauvegarde Wordpress depuis le SFTP.")
        restorewordpressfromsftp()
        menu()
    if choice == "4":
        print()
        print("Installation du monitoring Nagios\n")
        subprocess.call(['sh', './add-wordpress-to-monitor.sh'])
        menu()
    if choice == "5":
        print()
        print("Création d'une tache crontab pour la sauvegarde quotidienne du site wordpress\n")
        subprocess.call(['sh', './crontab.sh'])
        menu()
    if choice =="6":
        os.system("clear")
        exitmenu()
    while choice not in ["1","2","3","4","5","6"]:
        os.system("clear")
        print("La saisie (" + choice + ") n'est pas un choix valide, veuillez recommencer.")
        menu()
menu()
