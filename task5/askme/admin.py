from django.contrib import admin
from . import models

admin.site.register(models.Question)
admin.site.register(models.Tag)
admin.site.register(models.User)
admin.site.register(models.Mark2Answer)
admin.site.register(models.Mark2Question)
admin.site.register(models.Answer)
