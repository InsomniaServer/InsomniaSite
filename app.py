import json
import time

import cherrypy as cp

import user_database as users


class Webapp(object):
    """docstring for Webapp."""
    def __init__(self):
        users.tableSetup()

    @cp.expose(alias="home")
    def index(self):
        if 'logged_as' not in cp.session or cp.session['logged_as'] == None:
            htmlContent = ""
            with open("pages/home/not-connected.html") as page:
                for line in page:
                    htmlContent = htmlContent + line
            return htmlContent.format(img_mv="",img_rec="")
        else:
            htmlContent = ""
            with open("pages/home/connected.html") as page:
                for line in page:
                    htmlContent = htmlContent + line
            return htmlContent.format(name=users.getUserById(cp.session['logged_as'])[0]["name"],img_rec="", img_mv="")

    @cp.expose
    def login(self,fail=""):
        htmlContent = ""
        with open("pages/login/login.html") as page:
          line = " "
          while not line == "":
              line = page.readline()
              htmlContent = htmlContent + line
        return htmlContent.format(fail=fail,Nom_site="Site")

    @cp.expose
    def disconect(self):
        cp.session['logged_as'] = None
        return self.index()

    @cp.expose
    def signup(self,fail=""):
        htmlContent = ""
        with open("pages/signup/signup.html") as page:
          line = " "
          while not line == "":
              line = page.readline()
              htmlContent = htmlContent + line
        return htmlContent.format(fail=fail,Nom_site="Site")

    @cp.expose
    def login_status(self,mail,pwd):
        if users.checkUserExists(mail) and users.checkUserPassword(pwd, mail):
            cp.session['logged_as'] = users.getUserByMail(mail)[0]["id"]
            return  self.index()
        else:
            return self.login(fail="Erreur - Adresse et/ou mot de passe incorrect")

    @cp.expose
    def signup_status(self,name,mail,pwd,cpwd):
        if cpwd == pwd and not users.checkUserExists(mail):
            users.addUser(name,pwd,mail)
            cp.session['logged_as'] = users.getUserByMail(mail)[0]["id"]
            return self.index()
        else:
            error_message = ""
            if cpwd != pwd and users.checkUserExists(mail):
                error_message = "Erreur - Le mot de passe de confirmation n'est pas le même que le mot de passe choisi." \
                "Erreur - Addresse E-Mail déjà utilisée."
            elif cpwd != pwd:
                error_message = "Erreur - Le mot de passe de confirmation n'est pas le même que le mot de passe choisi."
            elif users.checkUserExists(mail):
                "Erreur - Addresse E-Mail déjà utilisée."
            return self.signup(fail=error_message)
