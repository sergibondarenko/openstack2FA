#!/usr/bin/python

import MySQLdb, pdb, pyotp, sys

class Log:
    def logging(self, var, msg):
        logfile = '/opt/stack/logs/mykeystone.log'
        myLog = open(logfile, 'a')
        myLog.write(var +'###  ')
        myLog.write(str(msg))
        myLog.write('\n')
        myLog.close()

LOG = Log()

class UserOtpInfo(object):

    def __init__(self, user_id):
        self.user_id = user_id
        self.mysqlhost = "localhost"
        self.mysqladmin = "root"
        self.mysqlpass = "password"
        self.mysqldb = "fastcloud"
        self.mysqltable = "horizon2fa_user"

    def qr(self, otp_secret):
        t = pyotp.TOTP(otp_secret)
        return str(t.now())

    def getotpuser(self):
        db = MySQLdb.connect(self.mysqlhost, self.mysqladmin, self.mysqlpass, self.mysqldb)
        cursor = db.cursor()
        cursor.execute("select * from " + self.mysqltable + " where user_id='" + self.user_id + "'")
        data = cursor.fetchone()
        db.close()
        return data

    def validate(self, pin):
        data = self.getotpuser()
        otp_secret = data[2]
        user_pin = self.qr(otp_secret)

        if user_pin != pin:
            LOG.logging('FAIL!', 0)
            sys.exit()
        else:
            LOG.logging('SUCCESS!', 0)

