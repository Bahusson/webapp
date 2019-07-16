from django.contrib import admin

from .models import Trick, Tech, Pageitem

admin.site.register(Pageitem)
admin.site.register(Trick)
admin.site.register(Tech)
# Register your models here.
