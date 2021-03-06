# -*- coding: utf-8 -*-

# Nox Obscura Guildpage
# ---------------------

from Servlet.Visitor import AbstractVisitor
from Servlet.Database.Raid import DataRaid
from Servlet.Database.User import DataUser

from mako.template import Template
import calendar, time

class Raidplaner(AbstractVisitor):
    """
    Provides the Raidplaner. The Visitor is able to logon on Raid-Events,
    with the options:
        1. signed
        2. substitude
        3. optout
        4. confimed (by admin user)
    Admin User is able to:
        1. create new raids
        2. confirm Visitors
        3. put Visitor in every other logon-state.
    The System automatically sends Mails to alle registred Visitors,
    if new Raids where created. If a Visitor is confirmed, the System sends
    him/her a nofification Mail. (Maybe notify all registred Visitors,
    which haven't yet changed her/his logon-State, eg. 2 Days before
    the event starts.
    """

    def __init__(self):
        # Do inheritance Stuff:
        AbstractVisitor.__init__(self)
        # Own Stuff:
        # DataRaid Instance:
        self.data = DataRaid()
        # calculate Today:
        self.today = self.calculateToday()

    def prettyPrintDate(self, x): # for functional map()
        dayNames = ["Mo, ", "Di, ", "Mi, ", "Do, ", "Fr, ", "Sa, ", "So, "]
        n = calendar.weekday(x[0], x[1], x[2])
        return dayNames[n] + unicode(x[2]) + "." + unicode(x[1]) + "." + unicode(x[0])

    def theNextTwelveDays(self):
        """Returns a List with Dates. Today is head and followed by the
        next 5 following dates. E.g.:
        [ [2011, 8, 23], ..., [2011,8,28] ]"""
        year = self.today[0]
        month = self.today[1]
        day = self.today[2]
        # Next 11 days, relative to today:
        c = calendar.monthcalendar(year, month)
        twelveDays = []
        for week in c:
            for iterDay in week:
                if (iterDay != 0) and (iterDay >= day and iterDay < day+12):
                    twelveDays.append( [year, month, iterDay] )
        if twelveDays.__len__() < 12: # Some days miss
            if month == 12: # Jump to the new Year
                year += 1
                cc = calendar.monthcalendar(year, 1)
            else: # If it's not year, then jump to the next Month
                month += 1
                cc = calendar.monthcalendar(year, month)
            for week in cc:
                for iterDay in week:
                    if (twelveDays.__len__() == 12): # enough days
                        break
                    if iterDay is not 0:
                        twelveDays.append( [year, month, iterDay] )
        if twelveDays.__len__() == 12:
            return twelveDays
        else:
            return False

    def getUsernamesAndPoints(self):
        data = DataUser()
        return data.getUsernamesAndPoints()

    def getFormularInfos(self, day):
        return self.data.getFormularInfosForRaid(self.username, day)

    def raidplaner(self):
        days = self.theNextTwelveDays()
        data = self.data
        myTmpl = Template(
            """<%include file="header.mako"/>
               <%include file="menu.mako"/>
               <%include file="content_head.mako"/>
               <%include file="raidplaner.mako"/>
               <%include file="points.mako"/>
               <%include file="content_foot.mako"/>
               <%include file="footer.mako"/>""",
            lookup=self.templateLookup)
        output = myTmpl.render_unicode(
            title="Nox Obscura: Raidplaner",
            cfg_staticPath=self.cfg.cfg_staticPath,
            cfg_siteUrl=self.cfg.cfg_siteUrl,
            anonymous=self.anonymous,
            theFirstSixDays=days[0:6],
            theFirstSixDaysPrettyPrinted=map(self.prettyPrintDate, days[0:6]),
            theSecondSixDays=days[6:12],
            theSecondSixDaysPrettyPrinted=map(self.prettyPrintDate, days[6:12]),
            getNameAndTimeForRaid=data.getNameAndTimeForRaid,
            admin=self.privileged,
            membersForDay=data.getLogonForRaidDate,
            getFormularInfos=self.getFormularInfos,
            usernamesAndPoints=self.getUsernamesAndPoints(),
            toCssAttr=self.toCssAttr)
        return output

