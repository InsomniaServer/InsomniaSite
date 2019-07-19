#!/usr/bin/python3.6
# -*- encoding: utf-8 -*-

# ---------------------------
# Import de librairies exterieures
# ---------------------------

import cherrypy
import os

# ---------------------------
# Import de fichiers locaux
# ---------------------------

from app import Webapp

# ---------------------------
# Configuration du serveur web
# ---------------------------

conf ={
    # Paramètres généraux
    '/':{
        # Utilisation des outils de sessions utilisateurs
        'tools.sessions.on':True,

        # Tous les chemins d'accès des fichiers sont exprimés par raport au dossier du programme
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static':{
        'tools.staticdir.on':True,
        'tools.staticdir.dir':'./static'
    }
}

# ---------------------------
# Config de Logging
# ---------------------------

cherrypy.config.update({
    # Desactive le log dans le terminal pour faire place à l'interface CLI
    'log.screen': False,

    # Redirige le log dans deux fichiers
    'log.access_file': 'access.log',
    'log.error_file': 'error.log'
})
cherrypy.config.update({'server.socket_port': 81})
# ---------------------------
# Lancement des diverse partie du programme
# ---------------------------

# Lancement global du serveur WEB
cherrypy.quickstart(Webapp(),"/",conf)

