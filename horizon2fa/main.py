import pyotp, qrcode, logging, os
from django.db import models
from StringIO import StringIO
from user import User


class Horizon2FA(models.Model):

    def otpConfirm(self, userid, user_otp):                          # WARNING

        u = User.get_user(userid)                          # WARNING

        if u is None:
            print("[Error]: Invalid user.")                          # WARNING
            return {"system": {"error": "Invalid user."}}                          # WARNING
        else:
            if u.verifyToken(user_otp):
                print("[Notice]: Authentication successful!")
                return {"route": "login.html"}
            else:
                print("[Error]: Invalid one-time token!")
                return {"route": "new.html"}

    def login(self, userid, user_otp):                          # WARNING
        """Login form."""

        u = User.get_user(userid)                          # WARNING		#CHECK SE PASSARE USERNAME O USERID
        if u is None:
            print("[Error]: Invalid user.")                          # WARNING
            return {"system": {"error": "Invalid user."}}                          # WARNING
        else:
            if u.authenticate(userid, user_otp):                          # WARNING
                print("[Notice]: Authentication successful!")
                return {"route": "view.html"}, u
            else:
                print("[Error]: Invalid one-time token!")
                return {"route": "login.html"}, u

    def code(self, userid):                          # WARNING
        """
        Returns the one-time password associated with the given user for the
        current time window. Returns empty string if user is not found.
        """
        u = User.get_user(userid)                          # WARNING

        if u is None:
            return ''

        t = pyotp.TOTP(u.key)
        return str(t.now())

#    def new(self, userid, key, password):
#        return User.create(userid, key, password)

    def new(self, userid, username, key):
        return User.create(userid, username, key)

    def save(self, u):
        return u.save()

    def qr(self, userid):
        """
        Return a QR code for the secret key associated with the userid
        The QR code is returned as file with MIME type image/png.
        """
        u = User.get_user(userid)
        if u is None:
            return ''
        t = pyotp.TOTP(u.key)
        issuer = u.username + "@Fastcloud"

        qr = qrcode.QRCode(version=2)
        qr.add_data(t.provisioning_uri(u.userid, issuer))
        qr.make()
        q = qr.make_image()
        img = StringIO()
        q.save(img)
        img.seek(0)
        return img
