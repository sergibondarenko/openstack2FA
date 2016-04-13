# The name of the panel to be added to HORIZON_CONFIG. Required.
PANEL = 'mypanel'

# The name of the dashboard the PANEL associated with. Required.
PANEL_DASHBOARD = 'identity'

# Python panel class of the PANEL to be added.
#ADD_PANEL = 'openstack_dashboard.dashboards.identity.mypanel.panel.MyPanel'
ADD_PANEL = 'myplugin.content.mypanel.panel.MyPanel'

# A list of applications to be prepended to INSTALLED_APPS
ADD_INSTALLED_APPS = ['myplugin']

## A list of AngularJS modules to be loaded when Angular bootstraps.
#ADD_ANGULAR_MODULES = ['horizon.dashboard.identity.myplugin.mypanel']
#
## Automatically discover static resources in installed apps
#AUTO_DISCOVER_STATIC_FILES = True
#
## A list of scss files to be included in the compressed set of files
#ADD_SCSS_FILES = ['dashboard/identity/myplugin/myplugin.scss']
