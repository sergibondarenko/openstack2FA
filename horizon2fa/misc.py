from keystoneclient.v3 import client
from keystoneauth1 import exceptions as keystone_exceptions
from user import User
import logging


LOG = logging.getLogger(__name__)


def getUsersList():
    keystone = client.Client(username='admin',
                             password='password',
                             project_name='admin',
                             auth_url='http://localhost:5000/v3')
    users_list = keystone.users.list()
    return users_list


def getUserName(user_id):
    users_list = getUsersList()
    u = next(( i for i in users_list if i.id == user_id), None)
    if u is None:
        return u
    else:
        return u.name


def getUserId(user_name):
    users_list = getUsersList()
    u = next(( i for i in users_list if i.name == user_name), None)
    if u is None:
        return u
    else:
        return u.id


def testUserAuthentication(userid, password):
    try:
        keystone = client.Client(user_id=userid,
                                 password=password,
                                 auth_url='http://localhost:5000/v3')
        return True

    except keystone_exceptions.http.Unauthorized:
        return False
