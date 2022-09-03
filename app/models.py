from django.db import models


class Word(models.Model):
    en = models.CharField(max_length=128, db_index=True)
    fa = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return f"{self.en} -> {self.fa}"


class Text(models.Model):
    title = models.CharField(max_length=128, db_index=True)
    content = models.TextField()
    words = models.ManyToManyField(Word) # Words that i don't know
    
    def __str__(self):
        return self.title
