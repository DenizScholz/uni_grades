from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View, generic
from .models import Gradebook, Grade
from .helpers import calcAverageGrades
from .forms import CustomUserCreationForm, GradebookCreationForm, GradeCreationForm


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@method_decorator(login_required, name='dispatch')
class Home(View):
    def get(self, request):
        gradebooks = Gradebook.objects.filter(owner=request.user)
        grades = Grade.objects.filter(gradebook__owner=request.user)

        for g in gradebooks:
            # TODO
            print(g.getHashID())

        context = {
            'gradebooks': gradebooks,
            'grades': grades,
            'average_grade': calcAverageGrades(grades),
            'total_creditpoints': Gradebook.getTotalCreditpointsGrades(grades),
        }
        return render(request, 'grade_app/home.html', context=context)


class About(View):
    def get(self, request):
        return render(request, 'base.html')


@method_decorator(login_required, name='dispatch')
class GradebookView(View):
    def get(self, request, pk):
        gradebook = Gradebook.objects.get(pk=pk)
        if not request.user == gradebook.owner:
            return HttpResponse('gtfo')

        grades = Grade.objects.filter(gradebook=gradebook)
        form = GradeCreationForm()

        context = {
            'gradebook': gradebook,
            'grades': grades,
            'form': form,
        }

        return render(request, 'grade_app/gradebook.html', context=context)

    def post(self, request, pk):
        # why does this work tho?
        gradebook = Gradebook.objects.get(pk=pk)
        if not request.user == gradebook.owner:
            return HttpResponse('gtfo')

        grades = Grade.objects.filter(gradebook=gradebook)
        form = GradeCreationForm(request.POST)

        if not form.is_valid():
            return HttpResponse('something sux')

        grade = form.save(commit=False)
        grade.gradebook = gradebook
        grade.save()
        form = GradeCreationForm()

        context = {
            'gradebook': gradebook,
            'grades': grades,
            'form': form,
        }
        
        return redirect('gradebook', pk=pk)


@method_decorator(login_required, name='dispatch')
class GradebookCreate(View):
    def get(self, request):
        form = GradebookCreationForm()
        return render(request, 'grade_app/gradebook-new.html', context={'form': form})

    def post(self, request):
        form = GradebookCreationForm(request.POST)

        if not form.is_valid():
            return HttpResponse('something sux')

        gradebook = form.save(commit=False)
        gradebook.owner = request.user
        gradebook.save()
        return redirect('home')
