from django.db import models


class Word(models.Model):
    en = models.CharField(max_length=128, db_index=True)
    line = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return self.word
