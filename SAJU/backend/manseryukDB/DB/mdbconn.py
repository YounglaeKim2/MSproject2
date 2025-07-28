import sqlite3
import datetime
import os

class SqliteDB():
    def __init__(self, db):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.conn = sqlite3.connect(self.BASE_DIR + '\\' + db)
        self.c = self.conn.cursor()

    def GetBirth(self, year, month, day):
        self.c.execute("SELECT * FROM calenda_data WHERE cd_sy='%s' and cd_sm='%s' and cd_sd='%s'" %(year, month, day))
        birthdata = self.c.fetchall()
        return birthdata

    def GetTime(self, time):
        jitime = [('子','자'),('丑','축'),('寅','인'),('卯','묘'),('辰','진'),('巳','사'),('午','오'),('未','미'),('申','신'),('酉','유'),('戌','술'),('亥','해')]
        if(time>23 or time<0):
            return ''
        ptime = time+1
        if(ptime==24): ptime=0
        itime = (int)(ptime/2)
        return jitime[itime]

    def Close(self):
        self.conn.close()
