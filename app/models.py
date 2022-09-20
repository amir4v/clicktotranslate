from django.db import models


class Word(models.Model):
    en = models.CharField(max_length=128, db_index=True)
    fa = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return f"{self.en} -> {self.fa}"


class Text(models.Model):
    title = models.CharField(max_length=128, db_index=True, unique=True)
    content = models.TextField()
    words_ik = models.ManyToManyField(Word, related_name='words_ik_text')   # Words that i know
    all_words = models.ManyToManyField(Word, related_name='all_words_text') # All-Words that it have
    
    def __str__(self):
        return self.title
