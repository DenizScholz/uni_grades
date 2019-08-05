from django.shortcuts import render, HttpResponse
from django.views import View
from .models import Gradebook, Grade


class Home(View):
    def get(self, request):
        gradebooks = Gradebook.objects.filter(owner=request.user)
        grades = Grade.objects.filter(gradebook__owner=request.user)
        # fix avg
        average_grade = [g.average_grade for g in gradebooks]
        return render(request, 'grade_app/home.html', context={'gradebooks': gradebooks, 'grades': grades, 'average_grade': average_grade})


class About(View):
    def get(self, request):
        return render(request, 'base.html')


class GradebookView(View):
    def get(self, request, pk):
        gradebook = Gradebook.objects.get(pk=pk)
        grades = Grade.objects.filter(gradebook=gradebook)
        if (request.user != gradebook.owner):
            return HttpResponse('not your gradebook')
        return render(request, 'grade_app/gradebook.html', context={'gradebook': gradebook, 'grades': grades})
