from django.db import models


# Create your models here.

class Students(models.Model):
    student_name = models.CharField(max_length=100)

    def __str__(self):
        return self.student_name


class Names(models.Model):
    rand_name = models.CharField(max_length=100)
    stu_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(Students, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.rand_name

    class Meta:
        ordering: ["-created_at"]

class LimitTime(models.Model):
    timer = models.IntegerField()

