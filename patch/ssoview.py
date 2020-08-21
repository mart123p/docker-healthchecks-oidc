from django.shortcuts import render

def fail(request):
    return render(request, "sso_fail.html")

