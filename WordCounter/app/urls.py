from django.urls import path
from django.views.generic import TemplateView

from .views import HomeView, WordView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('word/<int:pk>/', WordView.as_view(), name='word'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]
