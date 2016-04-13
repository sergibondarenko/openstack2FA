from django.utils.translation import ugettext_lazy as _
import horizon


class MyPanel(horizon.Panel):
    name = _("My Panel")
    slug = "mypanel"
