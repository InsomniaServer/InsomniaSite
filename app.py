import json

import cherrypy as cp
import mistune as mst

import user_database as users


class Webapp(object):
    """docstring for Webapp."""
    def __init__(self):
        users.tableSetup()

    @cp.expose(alias="home")
    def index(self):
        actus=[]
        with open("data.json") as datafile:
            actus=json.load(datafile)["actus"]
        actus_html=""
        for actu in actus:
            actu_body = ""
            with open("actus/" + actu["body"]) as content:
                actu_body=mst.markdown(content.read())
            actus_html = actus_html + """<div class='actu'>
            <h3>{title}</h3>
            <p>par {author} le {date}</p>
            {body}
            </div>""".format(title=actu['title'], author=actu['author'],
                             date=actu['date'],body=actu_body)
        if 'logged_as' not in cp.session or cp.session['logged_as'] == None:
            htmlContent = ""
            with open("pages/home/not-connected.html") as page:
                for line in page:
                    htmlContent = htmlContent + line
            return htmlContent.format(actus=actus_html)
        else:
            htmlContent = ""
            with open("pages/home/connected.html") as page:
                for line in page:
                    htmlContent = htmlContent + line
            return htmlContent.format(name=users.getUserById(cp.session['logged_as'])[0]["name"],actus=actus_html)

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
