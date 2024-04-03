import time

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import GetDataByUsernameForm
from .models import Account
from browserAutomation.seleniumDriver import TwoCaptchaSolve
from pathlib import Path

from django.middleware.csrf import get_token


def getDataByUsernameView(request):
    # если пришла инфа от формы
    if request.method == 'POST':
        form = GetDataByUsernameForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                # пытаемся по нику зацепить остальные данные
                data = Account.objects.get(username=username)
            except:
                time.sleep(1)
                return JsonResponse({'code': 400, 'message': 'Invalid username'})

            resolveByTwoCaptcha = TwoCaptchaSolve(user_data=data.serialize_data())
            login_result = resolveByTwoCaptcha.enter_process()
            try:
                return JsonResponse(login_result)
            except Exception as e:
                print(e)
                print(login_result)
                return JsonResponse({'code': 400, 'message': 'Something went wrong:/'})

    else:
        form = GetDataByUsernameForm()

    return render(request, 'enter_template.html', {'form': form})
