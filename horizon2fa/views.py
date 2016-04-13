import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from main import Horizon2FA


twoFA = Horizon2FA()


class IndexView(generic.TemplateView):
    template_name = 'identity/horizon2fa_panel/index.html'

def index(request):
    return render(request, 'horizon2fa/index.html', {})


def otpconfirm(request):
    if request.method == 'POST':
        try:
            result = twoFA.otpConfirm(request.POST['email'],\
                                    request.POST['otp'])

            if 'system' in result.keys():
                return result
            else:
                return HttpResponseRedirect('/login')

        except Exception as e:
            print("[Error]: Fail to confirm otp. Details: %s." % e)

    else:
        return render(request, 'horizon2fa/new.html', {})


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
                return render(request, 'horizon2fa/'
                              + result['route'], context)

        except Exception as e:
            print("[Error]: Fail to login on backend. Details: %s." % e)
            return render(request, 'horizon2fa/login.html', {})

    else:
        return render(request, 'horizon2fa/login.html', {})


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
            return render(request, 'horizon2fa/created.html', {'user':u})
        else:
            return HttpResponse('Invalid email or user already exists.')
    else:
        return render(request, 'horizon2fa/new.html')


def qr(request):
    return HttpResponse(twoFA.qr(request.GET.get("email")), content_type="image/png")
