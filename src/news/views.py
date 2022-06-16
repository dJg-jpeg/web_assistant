from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import NewsList

# Create your views here.
def index(request):
    return render(request, template_name='pages/index.html', context={'title': 'Web assistant'})

@login_required
def news(request):
    NL = NewsList.objects.all()
    context = {'NL': NL}
    return render(request, template_name='pages/news.html', context=context)