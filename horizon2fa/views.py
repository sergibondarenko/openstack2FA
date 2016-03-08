import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from main import Horizon2FA
from keystoneclient.v3 import client
from user import User
import misc


twoFA = Horizon2FA()


class IndexView(generic.TemplateView):
    template_name = 'horizon2fa_panel/index.html'


def index(request):
#    hz_user_name = request.user.username
#    hz_user_id = request.user.id
#    user_exists = False

#    if hz_user_name != 'admin':
    if request.user.username != 'admin':
        user_exists = misc.verify2fa(request)
#        keystone = client.Client(username='admin',
#                                 password='password',
#                                 project_name='admin',
#                                 auth_url='http://localhost:5000/v3')
#        user = keystone.users.get(hz_user_id) 
#        kc_user_email = str(user.email)

#        print "\n\n########## - Start of My Debug - ##########"
#        u = User.get_user(kc_user_email)
#        if u is None: # User is NOT registered for TFA
#            user_exists = False
#            print str(user_exists)
#            return render(request, 'horizon2fa_panel/index.html', { "user_exists":user_exists })
#        else: # User is already registered for TFA
#            user_exists = True
#            print str(user_exists)
#            return render(request, 'horizon2fa_panel/index.html', { "user_exists":user_exists })
        return render(request, 'horizon2fa_panel/index.html', { "user_exists":user_exists })
    else:
        return render(request, 'horizon2fa_panel/index.html', {})


def loginview(request):
    return render(request, 'horizon2fa_panel/login.html', {})


def newview(request):
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
        u = twoFA.new(request.POST['email'], None, request.POST['password'])

        if twoFA.save(u):
            return render(request, 'horizon2fa_panel/created.html', {'user':u})
        else:
            return HttpResponse('Invalid email or user already exists.')
    else:
        return render(request, 'horizon2fa_panel/new.html')


def qr(request):
    return HttpResponse(twoFA.qr(request.GET.get("email")), content_type="image/png")
