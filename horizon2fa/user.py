import pyotp
from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class User(models.Model):

    email = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    # https://docs.djangoproject.com/en/1.9/ref/models/instances/
    @classmethod
    def create(cls, email, key, password):
        u = cls(email=email, key=key, password=password)

        if u.key is None:
            u.key = pyotp.random_base32()

        return u

    def save(self):
        if len(self.email) < 1:
            return False

        try:
            u = User.objects.get(email=self.email)
            return False
        except ObjectDoesNotExist:
            super(User, self).save()
            return True

    def verifyToken(self, otp):
        t = pyotp.TOTP(self.key)
        return t.verify(otp)

    def authenticate(self, email, otp, passwd):
        try:
            u = User.objects.get(email=email)
            if passwd == u.password:
                return self.verifyToken(otp)
        except ObjectDoesNotExist:
            return False

    @classmethod
    def get_user(cls, email):
        try:
            u = User.objects.get(email=email)
            return u
        except ObjectDoesNotExist:
            return None
