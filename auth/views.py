from django.shortcuts import render
from ..blog_project.forms import RegistrationForm

# Create your views here.

def register(request) :
    form = RegistrationForm()

    context = {
        'form' : form,
    }
    return render(request, 'register.html', context)