from django.shortcuts import render, get_object_or_404

from .models import Job
from .models import Tech
from blog.models import Blog
from lotto.models import Lotto

def home(request):
    jobs = Job.objects
    return render(request, 'jobs/home.html', {'jobs':jobs})

def newsletter(request):
    blogs = Blog.objects
    jobs = Job.objects
    techs = Tech.objects
    progs = list(Lotto.objects.all())
    db3 = progs[-1]
    #detailblog = Blog.objects.all()[0]
    locations = list(Blog.objects.all())
    db1 = locations[-1]
    db2 = locations[-2]
#   detailblog = get_list_or_404(Blog)
    return render(request, 'jobs/newsletter.html', {'techs':techs, 'jobs':jobs, 'blogs':blogs, 'dblog':db1, 'cblog':db2, 'bblog':db3})

# Create your views here.
def books(request, jobs_id):
    books = get_object_or_404(Job, pk=jobs_id)
    return render(request, 'jobs/books.html', {'job':books})

def skills(request, techs_id):
    techs = Tech.objects
    skills = get_object_or_404(Tech, pk=techs_id)
    return render(request, 'techs/skills.html', {'tech':skills, 'techs':techs})
