# -*- coding: utf-8 -*-

# Nox Obscura Guildpage
# ---------------------

from Servlet.Database.User import DataUser

from mako.lookup import TemplateLookup
from mako.template import Template

import cherrypy

import Servlet.site_cfg

# E-Mail sende Funktion wird vererbt?? Oder in eine extra Klasse hier?

class AbstractVisitor(object):
    """
    It checks every Visitor via Cookie if he/she is:
        1. a anonymous Visitor
        2. a known Visitor (logged in)
            a. normal User
            b. privileged User
    And stores this Stateinfo for the Subclasses.
    """

    def __init__(self):
        # Template stuff (assumes that path from __main__):
        self.templateLookup = TemplateLookup(
            directories=['Servlet/Template', 'Servlet/Template/Content'],
            input_encoding='utf-8')
        # Make the Site Config available to all subclasses:
        self.cfg = Servlet.site_cfg
        # Lookup User and Session:
        self.username = "Anonymous"
        self.session = ""
        self.readCookie()
        # Check's if user is known and privileged:
        self.anonymous = self.checkAnonymity()
        self.privileged = self.checkPrivileges()

    def readCookie(self):
        cookie = cherrypy.request.cookie # Read Visitor's cookie.
        try:
            self.session = cookie['NoxSession'].value
            self.username = cookie['NoxUser'].value
        except: # Visitor has no cookie.
            pass

    def checkAnonymity(self):
        "False = known, True = unknown"
        data = DataUser()
        sessionInDb = data.retriveUsersSession(self.username)
        if self.session == sessionInDb:
            return False
        else:
            return True

    def checkPrivileges(self):
        "False = no admin, True = admin"
        data = DataUser()
        prv = data.retriveUsersPrivileges(self.username)
        if prv:
            return True
        else:
            return False

    def calculateToday(self):
        import time
        t = time.localtime() # time-struct.
        today = []
        today.append(t.tm_year)
        today.append(t.tm_mon)
        today.append(t.tm_mday)
        today.append(t.tm_hour)
        today.append(t.tm_min)
        today.append(t.tm_sec) # Save Dates in right order.
        return today

    def toCssAttr(self, x):
        if x == "Tank":
            return "roleTank"
        elif x == "Heiler":
            return "roleHeal"
        elif x == "Dps":
            return "roleDps"
        elif x == "Paladin":
            return "paladin"
        elif x == "Druide":
            return "druid"
        elif x == "Magier":
            return "mage"
        elif x == u"Jäger":
            return "hunter"
        elif x == "Schurke":
            return "rogue"
        elif x == "Hexenmeister":
            return "warlock"
        elif x == "Priester":
            return "priest"
        elif x == "Schamane":
            return "shaman"
        elif x == "Todesritter":
           return "deathknight"
        elif x == "Krieger":
           return "warrior"
        else:
           return "?"

    def errorPage(self, err):
        myTmpl = Template(
            """<%include file="header.mako"/>
               <%include file="menu.mako"/>
               <%include file="content_head.mako"/>
               <%include file="error_page.mako"/>
               <%include file="content_foot.mako"/>
               <%include file="footer.mako"/>""",
            lookup=self.templateLookup)
        output = myTmpl.render_unicode(
            title="Nox Obscura: Login",
            cfg_staticPath=self.cfg.cfg_staticPath,
            cfg_siteUrl=self.cfg.cfg_siteUrl,
            anonymous=self.anonymous,
            errMsg=err)
        return output

