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
    return render(request, 'horizon2fa_panel/index.html', {})


def loginview(request):
    return render(request, 'horizon2fa_panel/login.html', {})


def newview(request):
    return render(request, 'horizon2fa_panel/new.html', {})


def otpconfirm(request):
    if request.method == 'POST':
        try:
            result = twoFA.otpConfirm(request.POST['email'],                          # WARNING
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
            result, user = twoFA.login(request.POST['email'],                          # WARNING
                                       request.POST['otp'],
                                       request.POST['password'])

            if 'system' in result.keys():
                return result
            else:
                context = {'user': {'email': user.email}}                          # WARNING
                return render(request, 'horizon2fa_panel/'
                              + result['route'], context)

        except Exception as e:
            print("[Error]: Fail to login on backend. Details: %s." % e)
            return render(request, 'horizon2fa_panel/login.html', {})

    else:
        return render(request, 'horizon2fa_panel/login.html', {})


@csrf_exempt
def code(request):
    if request.method == 'POST':
        try:
            result = twoFA.code(request.POST['email'])                          # WARNING

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

        u = twoFA.new(userid, None, password)

        if twoFA.save(u):
            return render(request, 'horizon2fa_panel/created.html', {'user':u})
        else:
            return HttpResponse('User is invalid or already exists.')
    else:
        return render(request, 'horizon2fa_panel/new.html')


def qr(request):
    return HttpResponse(twoFA.qr(request.user.id), content_type="image/png")
