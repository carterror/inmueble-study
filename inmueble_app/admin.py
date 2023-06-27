from django.contrib import admin
from inmueble_app.models import Inmueble, Company, Comment

# Register your models here.

admin.site.register(Inmueble)
admin.site.register(Company)
admin.site.register(Comment)
