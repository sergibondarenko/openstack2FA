# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('horizon2fa', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Horizon2FA',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
