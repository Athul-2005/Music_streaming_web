from django.contrib import admin
from Musicapp.models import Songs, playlist, popularsongs

admin.site.register(Songs)
admin.site.register(playlist)
admin.site.register(popularsongs)
# Register your models here.
