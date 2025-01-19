from django.shortcuts import redirect
from django.utils.lorem_ipsum import words
from django.views.generic import CreateView

from .forms import CountingForm, WordForm
from .models import Counting, Word


class HomeView(CreateView):
    model = Counting
    form_class = CountingForm
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            counting = form.save()
            return redirect('word', pk=counting.pk)
        else:
            return self.form_invalid(form)


class WordView(CreateView):
    model = Word
    form_class = WordForm
    template_name = 'word.html'

    def form_valid(self, form):
        word = form.save(commit=False)
        if Word.objects.filter(word=word.word, counting_id=self.kwargs['pk']).exists():
            self.form_invalid(form)
            return redirect(self.get_success_url(), kwargs=self.kwargs)
        word.counting = Counting.objects.get(pk=self.kwargs['pk'])
        word.save()  # Сохраняем объект перед вызовом других методов
        word.word_count()  # Обновляем счетчик после сохранения
        return redirect(self.get_success_url(), kwargs=self.kwargs)

    def get_success_url(self):
        return f"{self.request.path}?word={self.request.POST.get('word')}"  # Переадресовываем на страницу со словом

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = self.request.GET.get('word')
        context['word'] = word
        if word:
            word = Word.objects.filter(
                word=word,
                counting_id=self.kwargs['pk']
            ).first()
            word.word_count()
            context['count'] = word.count
        return context
