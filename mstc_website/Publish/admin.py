from django.contrib import admin
from Publish.models import *

class DynamicsAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'publish_time')

class PartakeAdmin(admin.ModelAdmin):
	list_display = ('name', 'phone', 'event')

# Register your models here.
admin.site.register(Dynamics, DynamicsAdmin)
admin.site.register(Event)
admin.site.register(Tag)
admin.site.register(Partake, PartakeAdmin)