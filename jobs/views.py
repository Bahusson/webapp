from django.shortcuts import render

from .models import Job

from blog.models import Blog

def home(request):
    jobs = Job.objects
    return render(request, 'jobs/home.html', {'jobs':jobs})

def newsletter(request):
    blogs = Blog.objects
    return render(request, 'jobs/newsletter.html', {'blogs':blogs})

# Create your views here.
