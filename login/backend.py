# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Module defining the Django auth backend class for the Keystone API. """

import logging
from openstack_auth import exceptions
from openstack_auth import backend
from horizon2fa import misc, main

LOG = logging.getLogger(__name__)

KEYSTONE_CLIENT_ATTR = "_keystoneclient"

twoFA = main.Horizon2FA()


class MyKeystoneBackend(backend.KeystoneBackend):
    def authenticate(self, request=None, username=None, password=None,
                     user_domain_name=None, auth_url=None):

        user_id = misc.getUserId(username)
        user_email = misc.getUserEmail(user_id)    # TEMPORARY!!! REMOVE and use User_ID to verify Token!!!
        if user_id is None:
            raise exceptions.KeystoneAuthException("User not registered")

        if misc.verify2fa(user_id):    # User with 2FA
            LOG.info("USER " + username + "/" + user_id + " HAS OTP ENABLED..")
            user_password = password[:-6]
            user_otp = password[-6:]

            LOG.info("PASSWORD SPLITTED:")
            LOG.info("Password: " + user_password)
            LOG.info("OTP:" + user_otp)

            test2fa = twoFA.login(user_email, user_otp, user_password)

            if test2fa[0]['route'] == 'view.html':
                LOG.info("LOGIN 2FA Succesful!")
                return super(MyKeystoneBackend, self).authenticate(request=request,
                                                                   username=username,
                                                                   password=user_password,
                                                                   user_domain_name=user_domain_name,
                                                                   auth_url=auth_url)
            else:
                LOG.info("LOGIN 2FA Failed.....")
                raise exceptions.KeystoneAuthException("Token failed")

        else:                  # User WITHOUT 2FA
            LOG.info("USER " + username + " IS NOT PRESENT IN OTP DB!")
            return super(MyKeystoneBackend, self).authenticate(request=request,
                                                               username=username,
                                                               password=password,
                                                               user_domain_name=user_domain_name,
                                                               auth_url=auth_url)
