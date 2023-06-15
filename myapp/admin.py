from django.contrib import admin

from myapp import models

# Register your models here.
admin.site.register(models.work_types)
admin.site.register(models.customuser)
admin.site.register(models.schedule)
admin.site.register(models.appointment)
admin.site.register(models.Bill)
admin.site.register(models.card)
admin.site.register(models.complaints)