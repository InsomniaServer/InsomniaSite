import sqlite3 as sql
import hashlib as hasher
import codecs
import os

DB_PATH = 'db.db'

def tableSetup():
    """Setups the constants in the database"""
    try:
        with sql.connect(DB_PATH) as db:
            db.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                                              name TEXT,
                                              pwd_hash TEXT,
                                              mail TEXT)""")
            db.commit()
    except:
        pass


def addUser(sName, sPwd, sMail):
    """Adds an user into the database"""
    with sql.connect(DB_PATH) as db:
        sHashed=hasher.sha256(codecs.encode(sPwd)).hexdigest()
        db.execute("INSERT INTO users(name,pwd_hash,mail) VALUES (?,?,?)",(sName,sHashed,sMail))
        db.commit()


def removeUser(nUserID):
    """Delete an users from the database"""
    with sql.connect(DB_PATH) as db:
        db.execute("DELETE FROM users WHERE id=?",(nUserID,))
        db.commit()


def checkUserPassword(sGivenPwd, sMail):
    """Checks if a given password matches with the one of a given user"""
    sGPwdHash = hasher.sha256(codecs.encode(sGivenPwd)).hexdigest()
    sStoredHash = ""
    with sql.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("SELECT pwd_hash FROM users WHERE  mail=?",(sMail,))
        for info in cur:
            sStoredHash = info[0]
        cur.close()
    return sStoredHash == sGPwdHash


def checkUserExists(sMail):
    """Checks if a given e-mail adress is the one of a registered user"""
    nId = None
    with sql.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("SELECT id FROM users WHERE  mail=?",(sMail,))
        for info in cur:
            nId = info[0]
        cur.close()
    return nId is not None


def getUserByMail(sMail):
    """Gets all available info about the users corresponding to the given mail"""
    out = []
    with sql.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE  mail=?",(sMail,))
        for i in cur:
            out.append({
                "id": i[0],
                "name": i[1],
                "pwd_hash": i[2],
                "mail": i[3]
            })
        cur.close()
    if len(out) == 0: out.append({"Id": None, "Name": None, "Password Hash": None, "E-mail address": None})
    return out


def getUserById(nId):
    """Gets all available info about the user corresponding to the given id"""
    out = []
    with sql.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE  id=?",(nId,))
        for i in cur:
            out.append({
                "id": i[0],
                "name": i[1],
                "pwd_hash": i[2],
                "mail": i[3]
            })
        cur.close()
    if len(out) == 0: out.append({"Id": None, "Name": None, "Password Hash": None, "E-mail address": None})
    return out


def getUserByName(sName):
    """Gets all available info about all users whith a given name"""
    out = []
    with sql.connect(DB_PATH) as db:
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE  name=?",(sName,))
        for i in cur:
            out.append({
                "id": i[0],
                "name": i[1],
                "pwd_hash": i[2],
                "mail": i[3]
            })
        cur.close()
    if len(out) == 0: out.append({"Id": None, "Name": None, "Password Hash": None, "E-mail address": None})
    return out
