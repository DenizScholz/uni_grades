from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, get_object_or_404, get_list_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
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
        gradebook = get_object_or_404(Gradebook, pk=pk)
        if request.user == gradebook.owner:
            grades = Grade.objects.filter(gradebook=gradebook)
            form = GradeCreationForm()
            context = {
                'gradebook': gradebook,
                'grades': grades,
                'form': form,
            }
            return render(request, 'grade_app/gradebook.html', context=context)
        else:
            raise Http404("Not authorized")

    def post(self, request, pk):
        gradebook = get_object_or_404(Gradebook, pk=pk)
        if request.user == gradebook.owner:
            form = GradeCreationForm(request.POST)
            if form.is_valid():
                grade = form.save(commit=False)
                grade.gradebook = gradebook
                grade.save()
                return redirect('gradebook', pk=pk)
        else:
            raise Http404("Not authorized")


@method_decorator(login_required, name='dispatch')
class GradeView(View):
    def get(self, request, pk):
        grade = Grade.objects.get(pk=pk)
        gradebook = grade.gradebook
        if request.user == gradebook.owner:
            form = GradeCreationForm(instance=grade)
            context = {
                'form': form,
            }
            return render(request, 'grade_app/grade-new.html', context=context)
        else:
            raise Http404('Not authorized')

    def post(self, request, pk):
        grade = get_object_or_404(Grade, pk=pk)
        gradebook = grade.gradebook
        if request.user == gradebook.owner:
            form = GradeCreationForm(request.POST, instance=grade)
            if form.is_valid:
                form.save()
                return redirect('gradebook', pk=gradebook.pk)
            else:
                context = {
                    'form': form,
                }
                return render(request, 'grade_app/grade-new.html', context=context)
        else:
            raise Http404('Not authorized')


@method_decorator(login_required, name='dispatch')
class GradeDelete(View):
    def get(self, request, pk):
        grade = get_object_or_404(Grade, pk=pk)
        if request.user == grade.gradebook.owner:
            grade.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            raise Http404("Not authorized")


@method_decorator(login_required, name='dispatch')
class GradebookCreate(View):
    def get(self, request):
        form = GradebookCreationForm()
        return render(request, 'grade_app/gradebook-new.html', context={'form': form})

    def post(self, request):
        form = GradebookCreationForm(request.POST)
        if form.is_valid():
            gradebook = form.save(commit=False)
            gradebook.owner = request.user
            gradebook.save()
        return redirect('home')


@method_decorator(login_required, name='dispatch')
class GradebookDelete(View):
    def get(self, request, pk):
        gradebook = get_object_or_404(Gradebook, pk=pk)
        if request.user == gradebook.owner:
            gradebook.delete()
            return redirect('home')
        else:
            raise Http404("Not authorized")
