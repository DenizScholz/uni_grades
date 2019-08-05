from django.urls import path, include
from .views import Home, About, GradebookView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('gradebook/<int:pk>/', GradebookView.as_view(), name='gradebook'),
]
