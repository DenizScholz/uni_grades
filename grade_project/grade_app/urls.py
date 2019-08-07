from django.urls import path, include
from .views import Home, About, GradebookView, SignUp, GradebookCreate, GradeDelete

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('grade/<int:pk>/delete/', GradeDelete.as_view(), name='grade-delete'),
    path('gradebook/<int:pk>/', GradebookView.as_view(), name='gradebook'),
    path('gradebook/create/', GradebookCreate.as_view(), name='gradebook-create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUp.as_view(), name='signup'),
]
