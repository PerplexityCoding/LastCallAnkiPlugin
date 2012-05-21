
from aqt import mw

import os, pickle, codecs, shutil, time
from datetime import datetime
from anki.hooks import addHook

class LastCall:
        ################# CUSTOMIZE ###################
    Profiles = {
        "DEFAULT" : { #Profile by default, in Hour
            "LastCallHour" : 22
        },
        "FanAtiC" : { #Other Profile Name
            "LastCallHour" : 21
        }
        # Add other Profile name
    }
    ################################################
    
    def load(self):
        
        profileName = mw.pm.name
        pf = self.Profiles
        profileVar = pf["DEFAULT"] if not profileName in pf else pf[profileName]
        
        LastCallHour = profileVar["LastCallHour"]
        
        hour = datetime.fromtimestamp(mw.col.crt).hour
        now = time.time() - hour * 3600
        nowDate = datetime.fromtimestamp(now)
        
        LastCallDate = nowDate.replace(hour = LastCallHour - hour, minute = 0, second = 0)
        LastCall = time.mktime(LastCallDate.timetuple())
        
        nextDayDate = nowDate.replace(hour = 23, minute = 59, second = 59)
        nextDay = time.mktime(nextDayDate.timetuple())
        
        log(str(nowDate))
        log(str(LastCallDate))
        log(str(nextDayDate))
        
        self.oldCollapseTime = None
        
        if now >= LastCall and now <= nextDay:
            
            log("This is Last Call !")
            collapseTime = int(nextDay - now)
            
            self.oldCollapseTime = mw.col.conf['collapseTime']
            mw.col.conf['collapseTime'] = min(max(collapseTime, 0), 24 * 3600) #min, max is protection, look 24h max in advance
            log(mw.col.conf['collapseTime'])
            
            mw.col.setMod()  
            mw.col.save()

    def unload(self):
        if self.oldCollapseTime:
            mw.col.conf['collapseTime'] = self.oldCollapseTime
            mw.col.setMod()
            mw.col.save()
            
            log(str(mw.col.conf['collapseTime']))


def log(msg):
    logPath = os.path.join(mw.pm.addonFolder(), 'lcol-main.log')
    txt = '%s: %s' % (datetime.now(), msg)
    f = codecs.open(logPath, 'a', 'utf-8')
    f.write(txt + '\n')
    f.close()

lastCall = LastCall()
addHook("profileLoaded", lastCall.load)
addHook("unloadProfile", lastCall.unload)

