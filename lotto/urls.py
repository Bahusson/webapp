from django.urls import path

from . import views
from . import randomize

urlpatterns = [
    path('', views.download, name='download'),
    path('<int:lotto_id>/', views.progpage, name='progpage'),
    path('lotto/pybrun/', views.pybrun, name='pybrun'),
    path('lotto/pybrun/roll', randomize.roll, name='roll'),
]
