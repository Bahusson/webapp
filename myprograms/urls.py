from django.urls import path
from . import views

urlpatterns = [
    path('', views.download, name='download'),
    path('<int:myprogram_id>/', views.progpage, name='progpage'),
    path('myprogram/pybrun/', views.pybrun, name='pybrun'),
#    path('myprogram/roll/', views.roll, name='roll'),
    path('myprogram/pybrun/<int:myprogram_id>/', views.progpage, name='progpage'),
]
