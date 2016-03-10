import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from main import Horizon2FA
from keystoneclient.v3 import client
from user import User
import misc, pdb


twoFA = Horizon2FA()


class IndexView(generic.TemplateView):
    template_name = 'horizon2fa_panel/index.html'


def index(request):
    if request.user.username != 'admin':
        user_exists = misc.verify2fa(request.user.id)
        return render(request, 'horizon2fa_panel/index.html', { "user_exists":user_exists })
    else:
        return render(request, 'horizon2fa_panel/index.html', {})


def loginview(request):
    return render(request, 'horizon2fa_panel/login.html', {})


def newview(request):
    if request.user.username != 'admin':
        user_email = misc.getUserEmail(request.user.id)
        return render(request, 'horizon2fa_panel/new.html', { "user_email":user_email })
    else:
        return render(request, 'horizon2fa_panel/new.html', {})


def otpconfirm(request):
    if request.method == 'POST':
        try:
            result = twoFA.otpConfirm(request.POST['email'],\
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
            result, user = twoFA.login(request.POST['email'],
                                       request.POST['otp'],
                                       request.POST['password'])

            if 'system' in result.keys():
                return result
            else:
                context = {'user': {'email': user.email}}
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
            result = twoFA.code(request.POST['email'])

            if len(result) > 0:
                return HttpResponse(json.dumps(result),
                            content_type = "application/json")

        except Exception as e:
            print("[Error]: Fail to get codes. Details: %s." % e)


def new(request):
    """New user form."""
    if request.method == 'POST':
        #pdb.set_trace()
        if 'email' in request.POST:
            u = twoFA.new(request.POST['email'], None, request.POST['password'])
        else:
            u = twoFA.new(misc.getUserEmail(request.user.id), None, request.POST['password'])

        invalid = misc.testUserAuthentication(request.user.id, request.POST['password'])
#        if twoFA.save(u):
#            return render(request, 'horizon2fa_panel/created.html', {'user':u})
#        else:
#            return HttpResponse('Invalid email or user already exists.')
#    else:
#        return render(request, 'horizon2fa_panel/new.html')
        return render(request, 'horizon2fa_panel/new.html',  { "invalid":invalid })


def qr(request):
    eeturn HttpResponse(twoFA.qr(request.GET.get("email")), content_type="image/png")
