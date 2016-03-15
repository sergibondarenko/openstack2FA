import pyotp
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class User(models.Model):

    userid = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    key = models.CharField(max_length=50)

    # https://docs.djangoproject.com/en/1.9/ref/models/instances/
    @classmethod
    def create(cls, userid, username, key):
        u = cls(userid=userid, username=username, key=key)

        if u.key is None:
            u.key = pyotp.random_base32()

        return u

    def save(self):
        if len(self.userid) < 1:
            return False

        try:
            u = User.objects.get(userid=self.userid)
            return False
        except ObjectDoesNotExist:
            super(User, self).save()
            return True

    def verifyToken(self, otp):
        t = pyotp.TOTP(self.key)
        return t.verify(otp)

    def authenticate(self, userid, otp):
        try:
            u = User.objects.get(userid=userid)
            return self.verifyToken(otp)
        except ObjectDoesNotExist:
            return False

    @classmethod
    def get_user(cls, userid):
        try:
            u = User.objects.get(userid=userid)
            return u
        except ObjectDoesNotExist:
            return None
