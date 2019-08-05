from django.db import models
from django.conf import settings


class Gradebook(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def average_grade(self):
        grades = Grade.objects.filter(gradebook=self)
        if not grades:
            return 0
        result = 0
        for g in grades:
            result += g.value
        return result/len(grades)


class Grade(models.Model):
    gradebook = models.ForeignKey(Gradebook, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    creditpoints = models.IntegerField(default=6)
    value = models.DecimalField(max_digits=2, decimal_places=1, default=1.0)
    weighted = models.BooleanField(default=True)

    def __str__(self):
        return self.title
