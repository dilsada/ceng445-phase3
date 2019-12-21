from django.db import models
from django_matplotlib.fields import MatplotlibFigureField


class BoardModel(models.Model):
    bid = models.CharField(max_length=10, primary_key=True)
    bname = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.bname

class MyModelWithFigure(models.Model):
    figure = MatplotlibFigureField(figure='my_figure')