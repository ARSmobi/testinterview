from itertools import count

from django.db import models


class Counting(models.Model):
    name = models.CharField(max_length=64)
    text_file = models.FileField(upload_to='media/')


class Word(models.Model):
    word = models.CharField(max_length=64)
    count = models.IntegerField(default=0, null=True)
    counting = models.ForeignKey(Counting, on_delete=models.CASCADE)

    def word_count(self):
        with open(self.counting.text_file.path, 'r') as txt_file:
            txt = txt_file.read()
        self.count = txt.lower().count(str(self.word).lower())
        self.save()
