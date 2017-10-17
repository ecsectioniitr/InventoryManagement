from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Equipment)
admin.site.register(EquipmentInstance)
admin.site.register(Issueance)
admin.site.register(Follow)
