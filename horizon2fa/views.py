import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from main import Horizon2FA
from keystoneclient.v3 import client
from user import User
import misc, pdb, logging


twoFA = Horizon2FA()

LOG = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = 'horizon2fa_panel/index.html'


def index(request):
    u = User.get_user(request.user.id)

    if u is None:
        return render(request, 'horizon2fa_panel/index.html', { "user_exists":False })
    else:
        return render(request, 'horizon2fa_panel/index.html', { "user_exists":True })


def loginview(request):
    return render(request, 'horizon2fa_panel/login.html', {})


def newview(request):
    return render(request, 'horizon2fa_panel/new.html', {})


def otpconfirm(request):
    if request.method == 'POST':
        try:
            result = twoFA.otpConfirm(request.POST['userid'],                          # WARNING
                                    request.POST['otp'])

            if 'system' in result.keys():
                return result
            else:
                return HttpResponseRedirect('login')

        except Exception as e:
            print("[Error]: Fail to confirm otp. Details: %s." % e)

    else:
        return render(request, 'horizon2fa_panel/new.html', {})


def login(request):
    user = None

    if request.method == 'POST':
        try:
            result, user = twoFA.login(request.user.id, request.POST['otp'])

            if 'system' in result.keys():
                return result
            else:
                context = {'user': {'id': request.user.id}}                          # WARNING
                return render(request, 'horizon2fa_panel/'
                              + result['route'], context)

        except Exception as e:
            print("[Error]: Fail to login on backend. Details: %s." % e)
            return render(request, 'horizon2fa_panel/login.html', {})

    else:
        return render(request, 'horizon2fa_panel/login.html', {})

#        try:
#            result, user = twoFA.login(request.POST['email'],                          # WARNING
#                                       request.POST['otp'],
#                                       request.POST['password'])
#
#            if 'system' in result.keys():
#                return result
#            else:
#                context = {'user': {'email': user.email}}                          # WARNING
#                return render(request, 'horizon2fa_panel/'
#                              + result['route'], context)
#
#        except Exception as e:
#            print("[Error]: Fail to login on backend. Details: %s." % e)
#            return render(request, 'horizon2fa_panel/login.html', {})
#
#    else:
#        return render(request, 'horizon2fa_panel/login.html', {})


@csrf_exempt
def code(request):
    if request.method == 'POST':
        LOG.debug("##############" + request.POST['userid'])
        try:
            result = twoFA.code(request.POST['userid'])                          # WARNING

            if len(result) > 0:
                return HttpResponse(json.dumps(result),
                            content_type = "application/json")

        except Exception as e:
            print("[Error]: Fail to get codes. Details: %s." % e)


def new(request):
    """New user form."""
    if request.method == 'POST':
        userid = request.user.id
        password = request.POST['password']
        username = misc.getUserName(userid)

        if misc.testUserAuthentication(userid, password):
            u = twoFA.new(userid, username, None)
            if twoFA.save(u):
                return render(request, 'horizon2fa_panel/created.html', {'user':u})
            else:
                return render(request, 'horizon2fa_panel/new.html', { "invalid":False, "user_exists":True })
        else:
            return render(request, 'horizon2fa_panel/new.html', { "invalid":True, "user_exists":False })

    else:
        return render(request, 'horizon2fa_panel/new.html')


def qr(request):
    return HttpResponse(twoFA.qr(request.user.id), content_type="image/png")
