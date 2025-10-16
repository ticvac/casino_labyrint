from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(GraphPoint)
admin.site.register(PointVisit)
admin.site.register(Transaction)
admin.site.register(Game)
admin.site.register(ReachedZero)  # hot fix
admin.site.register(Achievement)