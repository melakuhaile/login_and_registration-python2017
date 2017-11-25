from django.shortcuts import render, redirect
from django.contrib import messages
from models import User 

# Create your views here.

def index(request):

    return render (request, 'loginInfo/index.html')



def success(request,first_name):
    context = {
        "first_name": first_name
    }
    return render(request,'loginInfo/success.html', context)


def registration(request):
    print "Here's the post request:"
    print request.POST
    results = User.manager.makeUser(request.POST)
    if results[0]:
        return redirect('/success/{}'.format(results[1].first_name))

    for message in results[1].itervalues():
        messages.error(request, message)
    return redirect('/')


def login(request):
    results = User.manager.UserLogin(request.POST)
    if results[0]:
        return redirect('/success/{}'.format(results[1].first_name))

    for message in results[1].itervalues():
        messages.error(request, message)
    return redirect('/')
