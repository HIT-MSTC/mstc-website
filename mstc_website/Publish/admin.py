from django.contrib import admin
from Publish.models import *

class DynamicsAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'publish_time')

class PartakeAdmin(admin.ModelAdmin):
	list_display = ('name', 'phone', 'event')

class ImgAdmin(admin.ModelAdmin):
	list_display = ('name', 'author', 'uptime')
# Register your models here.
admin.site.register(Dynamics, DynamicsAdmin)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Partake, PartakeAdmin)
admin.site.register(Img, ImgAdmin)