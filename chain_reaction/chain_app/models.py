from django.db import models


class Board(models.Model):
    bid = models.CharField(max_length=10, primary_key=True)
    bname = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.bname
