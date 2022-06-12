from django.contrib.auth.hashers import check_password
from django.contrib.messages import info
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, template_name='pages/index.html', context={'title': 'Web assistant'})


def registration(request):
    context = {
        'form': SignUpForm(),
    }
    if request.method == "POST":
        context['form'] = SignUpForm(request.POST)
        if context['form'].is_valid():
            context['form'].save()
            return redirect('login')
    return render(request, template_name='pages/registration.html', context=context)


def login_user(request):
    context = {
        'form': LoginForm(),
    }
    if request.method == "POST":
        context['form'] = LoginForm(request.POST)
        if context['form'].is_valid():
            username = context['form'].cleaned_data['username']
            password = context['form'].cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user and check_password(password, user.password):
                login(request, user)
                return redirect('index')
        info(request, 'Username or password is incorrect')
    return render(request, template_name='pages/login.html', context=context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('index')
