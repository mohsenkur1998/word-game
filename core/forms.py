from django import forms


class StudentForm(forms.Form):
    student_name = forms.CharField(label="Enter name", max_length=100)
