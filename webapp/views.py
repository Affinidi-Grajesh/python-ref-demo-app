from django.shortcuts import render



# Create your views here.
def home(request):
    return render(request, "webapp/home.html")

def cis(request):
    return render(request, "webapp/cis.html")

def iota(request):
    return render(request, "webapp/iota.html")

def revoke(request):
    return render(request, "webapp/revoke.html")

def verify(request):
    return render(request, "webapp/verify.html")

def completed(request):
    return render(request, "webapp/completed.html")


