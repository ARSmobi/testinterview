from django import forms

from .models import Counting, Word


class CountingForm(forms.ModelForm):
    class Meta:
        model = Counting
        fields = ['name', 'text_file']


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['word']
