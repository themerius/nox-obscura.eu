# -*- coding: utf-8 -*-

# Nox Obscura Guildpage
# ---------------------

from Servlet.Database import AbstractData

class DataRaid(AbstractData):
    """
    Creates and maintaines the Raid specific Datastructures.
    """
    def __init__(self):
        # Inheritance Stuff
        AbstractData.__init__(self)
        # Set the Default DB for this Class
        self.myDefaultDb = self.raids

    def newRaidEvent(self, name, date, time):
        """name must be string,
        date must be [year, month, day] eg [2011,8,24]
        time must be string eg "19:15"
        """
        counter = self.readEntry('counter')
        counter = counter['eventCounter']
        # Generate new Data and put it in Db
        data = {"name": name, "date": date, "time": time, "type": "raidEvent"}
        newEntry = self.createNewEntry( data, "event"+str(counter) )
        if newEntry:
            # count up the Counter in Db
            self.changeOneEntry('counter', 'eventCounter', counter+1 )

    def newOrChangeRaidLogon(self, raidId, username, charName,
            state, comment, role, class_):
        data = {'raidId': raidId,
                'username': username,
                'charName': charName,
                'state': state,
                'comment': comment,
                'role': role,
                'class': class_,
                'type': 'raidLogon'}
        view = self.readView("raids-3", key=[raidId,username])
        if view: # Only change Logon
            self.changeEntireEntry(view[0].id, data)
        else: # Create New Entry
            counter = self.readEntry('counter')
            counter = counter['logonCounter']
            newEntry = self.createNewEntry(data, "logon"+str(counter))
            if newEntry:
                self.changeOneEntry('counter', 'logonCounter', counter+1)

    def getLogonForRaidDate(self, logon, raidDate):
        view = self.readView('raids-2', key=raidDate)
        if view:
            raidId = view[0].value
            viewLogon = self.readView('raids-4', key=[raidId,logon])
            if viewLogon:
                return viewLogon
            else:
                return []
        else:
            return []

    def getNameAndTimeForRaid(self, raidDate):
        view = self.readView('raids-2', key=raidDate)
        if view:
            raidId = view[0].value
            data = self.readEntry(raidId)
            name = data['name']
            time = data['time']
            return [name, time]
        else:
            return ["", ""]
