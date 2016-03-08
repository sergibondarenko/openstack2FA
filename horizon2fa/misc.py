from keystoneclient.v3 import client
from user import User


def verify2fa(request):
    hz_user_name = request.user.username
    hz_user_id = request.user.id
    user_exists = False

    keystone = client.Client(username='admin',
                             password='password',
                             project_name='admin',
                             auth_url='http://localhost:5000/v3')
    user = keystone.users.get(hz_user_id)
    kc_user_email = str(user.email)

    u = User.get_user(kc_user_email)
    if u is None: # User is NOT registered for TFA
        user_exists = False
        return user_exists
    else: # User is already registered for TFA
        user_exists = True
        return user_exists
