# openstack2FA

#### Installation steps

Install python dependencies
 * sudo pip install pyotp qrcode pillow

Build and install the plugin
 * python <path>/openstack2FA/setup.py sdist
 * cp <path>/openstack2FA/horizon2fa/enabled/_31005_horizon2fa.py <path>/horizon/openstack_dashboard/local/enabled/
 * sudo pip install <path>/openstack2FA/dist/horizon2fa-0.1.tar.gz

