from keystoneclient.v3 import client
from keystoneauth1 import exceptions as keystone_exceptions
from user import User


def getUserEmail(user_id):
    keystone = client.Client(username='admin',
                             password='password',
                             project_name='admin',
                             auth_url='http://localhost:5000/v3')
    try:
        user = keystone.users.get(user_id)
        return str(user.email)
    except ObjectDoesNotExist:
        return None


def verify2fa(user_id):
    user_email = getUserEmail(user_id)
    if user_email is None:
        return True # WARNING - Temporary workaround
    else:
        u = User.get_user(user_email)
        if u is None: # User is NOT registered for TFA
            return False
        else: # User is _already registered for TFA
            return True


def testUserAuthentication(username, password):
    try:
        keystone = client.Client(username=username, password=password, auth_url='http://localhost:5000/v3')
        return False
    except keystone_exceptions.http.Unauthorized:
        return True
