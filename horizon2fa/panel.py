from django.utils.translation import ugettext_lazy as _
import horizon


class Horizon2faPanel(horizon.Panel):
    name = _("Two-Factor Auth")
    slug = "horizon2fa_panel"
