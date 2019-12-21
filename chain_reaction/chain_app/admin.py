from django.contrib import admin
from .models import BoardModel, MyModelWithFigure
# Register your models here.

admin.site.register(BoardModel)
admin.site.register(MyModelWithFigure)
