# openstack2FA

#### Installation steps

Install python dependencies
 * sudo pip install pyotp qrcode pillow

Configure the MySQL database
 * create a MySQL database (ex: fastcloud) and user with privileges (ex: fastcloud/password)
 * add the database configuration to <path>/horizon/openstack_dashboard/local/local_settings.py (see local_settings.py.example)
````python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fastcloud',
        'USER': 'fastcloud',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
````

Build and install the plugin
 * python <path>/openstack2FA/setup.py sdist
 * cp <path>/openstack2FA/horizon2fa/enabled/_31005_horizon2fa.py <path>/horizon/openstack_dashboard/local/enabled/
 * sudo pip install <path>/openstack2FA/dist/horizon2fa-0.1.tar.gz

