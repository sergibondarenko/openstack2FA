import pyotp, qrcode, logging, os
from django.db import models
from StringIO import StringIO
from user import User


class Horizon2FA(models.Model):

    def otpConfirm(self, user_email, user_otp):                          # WARNING

        u = User.get_user(user_email)                          # WARNING

        if u is None:
            print("[Error]: Invalid email address.")                          # WARNING
            return {"system": {"error": "Invalid email address."}}                          # WARNING
        else:
            if u.verifyToken(user_otp):
                print("[Notice]: Authentication successful!")
                return {"route": "login.html"}
            else:
                print("[Error]: Invalid one-time token!")
                return {"route": "new.html"}

    def login(self, user_email, user_otp, user_pass):                          # WARNING
        """Login form."""

        u = User.get_user(user_email)                          # WARNING
        if u is None:
            print("[Error]: Invalid email address.")                          # WARNING
            return {"system": {"error": "Invalid email address."}}                          # WARNING
        else:
            if u.authenticate(user_email, user_otp, user_pass):                          # WARNING
                print("[Notice]: Authentication successful!")
                return {"route": "view.html"}, u
            else:
                print("[Error]: Invalid password or one-time token!")
                return {"route": "login.html"}, u

    def code(self, user_email):                          # WARNING
        """
        Returns the one-time password associated with the given user for the
        current time window. Returns empty string if user is not found.
        """
        u = User.get_user(user_email)                          # WARNING

        if u is None:
            return ''

        t = pyotp.TOTP(u.key)
        return str(t.now())

    def new(self, userid, key, password):
        return User.create(userid, key, password)

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
        q = qrcode.make(t.provisioning_uri(u.userid))
        img = StringIO()
        q.save(img)
        img.seek(0)
        return img
