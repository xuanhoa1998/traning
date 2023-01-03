from urllib import request

from django.contrib.auth.views import LoginView
from django.shortcuts import render


def login(request):
    a = 1
    context = {}
    context.update(
        {
            "a": a,
        }
    )
    return render(
        request=request,
        template_name="user/login.html",
        context=context,
    )

