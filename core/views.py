import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import random
import time
import threading
from datetime import datetime, timedelta
from textblob import Word
from .models import Students, Names, LimitTime
from django.contrib import messages


# Create your views here.

def index(request):
    if request.method == "POST":
        limit_timer = request.POST['timer']
        LimitTime.objects.create(timer=limit_timer)
        return redirect("students")
    else:
        return render(request, 'core/homepage.html')


def first_pick(request):
    names = ["apple", "banana", "orange", "pick", "random", "lamp", "dad", "cat", "dog", "hair", "behalf", "wash",
             "play", "tell", "fallen", "go", "bar", "dress", "you", "now"]
    name_picker = random.choice(names)
    last_word = name_picker[-1]
    Names.objects.create(rand_name=name_picker)
    if request.method == "POST":
        limit_timer = request.POST['timer']
        LimitTime.objects.create(timer=limit_timer)
        return redirect("pick")
    else:
        return render(request, "core/new_first.html", {"name": name_picker, "last": last_word})


"""
optional make a teacher role too
that students won't write the word. delete all words and student at the end.another option is to count the marks for each student.
add stop timer and 
"""


def pick_name(request):
    all_words = Names.objects.all()
    stored_name = Names.objects.last()
    picked_name = stored_name.rand_name
    last_picked_word = picked_name[-1]

    students_all = Students.objects.all()

    all_names = []
    for name in students_all:
        all_names.append(name.student_name)

    get_time = LimitTime.objects.last()
    time_limit = get_time.timer
    print(type(time_limit))
    end_time = time.time() + time_limit

    request.session['end_time'] = end_time
    end_time = request.session.get('end_time')

    if end_time and end_time < time.time():
        request.session['end_time'] = None
        print(end_time)

    if request.method == 'POST':
        submitted_word = request.POST["words"]
        submitted_name = request.POST.get("stu")

        word = Word(submitted_word)
        spel = word.spellcheck()
        first_word = submitted_word[0]
        if last_picked_word == first_word:
            if word == spel[0][0]:
                messages.success(request, "correct")
                Names.objects.create(rand_name=submitted_word, stu_name=submitted_name)
                return redirect("result")

            else:
                messages.error(request, f'Correct spelling of "{word}": "{spel[0][0]}" (with {spel[0][1]} confidence).')
                return redirect("pick")
        else:
            messages.error(request, "not same")
            get_stu = Students.objects.get(student_name=submitted_name)
            get_stu.delete()
            return redirect("pick")

    else:
        stud = request.GET.get('dataa')
        names = Students.objects.filter(student_name=stud)
        print(stud)
        if Students.objects.filter(student_name=stud).exists():
            print(stud)
            names.delete()

        else:
            messages.error(request, "not found")
            print(stud)

        return render(request, "core/new_name.html", {"name": picked_name, "last": last_picked_word,
                                                   "all": all_words, "all_names": all_names, "time": time_limit
                                                   })


# def name_delete(request, student):
# student = request.GET.get('dataa')
# names = Students.objects.filter(student_name=student)
# print(student)
# if Students.objects.filter(student_name=student).exists():
#     print(student)
#     names.delete()
#     return JsonResponse({'status': 'student deleted'})
# else:
#     print(student)
#     return JsonResponse({'status': 'none'})


def result(request):
    result_name = Names.objects.last()
    str_name = str(result_name)
    last_word = str_name[-1]

    all_words = Names.objects.all()
    students_all = Students.objects.all()
    words = []
    for n in all_words:
        words.append(n.rand_name)

    all_names = []
    for name in students_all:
        all_names.append(name.student_name)

    get_time = LimitTime.objects.last()
    time_limit = get_time.timer
    end_time = time.time() + time_limit

    request.session['end_time'] = end_time
    end_time = request.session.get('end_time')

    if end_time and end_time < time.time():
        request.session['end_time'] = None
        print(end_time)


    if request.method == 'POST':
        submitted_word = request.POST["words"]
        submitted_name = request.POST.get("stu")
        word = Word(submitted_word)
        spel = word.spellcheck()

        if last_word == submitted_word[0]:
            if submitted_word not in words:
                if word == spel[0][0]:

                    messages.success(request, "correct")
                    Names.objects.create(rand_name=submitted_word, stu_name=submitted_name)
                    return redirect("result")

                else:

                    messages.error(request,
                                   f'Correct spelling of "{word}": "{spel[0][0]}" (with {spel[0][1]} confidence).')
                    return redirect("result")
            else:
                messages.error(request, "repetitive")
                return redirect("result")
        else:

            messages.error(request, "not same")
            get_stu = Students.objects.get(student_name=submitted_name)
            get_stu.delete()
            return redirect("result")

    else:
        stud = request.GET.get('dataa')
        names = Students.objects.filter(student_name=stud)
        print(stud)
        if Students.objects.filter(student_name=stud).exists():
            print(stud)
            names.delete()

        else:
            messages.error(request, "not found")
            print(stud)

        student_count = Students.objects.count()
        aggregate_names = Names.objects.distinct("stu_name")
        word_names = []
        for name in aggregate_names:
            words = Names.objects.filter(stu_name=name.stu_name)
            word_count = words.count()
            word_names.append({"stu_name": name.stu_name, "rand_name": words, "word_count": word_count})
        if student_count == 1:
            last_student = Students.objects.last()
            return render(request, "core/new_final.html", {"winner": last_student, "all_words": word_names})
        return render(request, "core/new_result.html", {"results": result_name, "last": last_word,
                                                    "words": all_words, "names": all_names})


def random_name(request):
    # if 'end_time' not in request.session:
    #     request.session['end_time'] = None
    datas = Students.objects.order_by('?').first()
    # names = []
    # for name in datas:
    #     names.append(name.student_name)
    #
    # random_picker = random.sample(names, 1)
    # return HttpResponse(random_picker)
    if request.method == 'POST':
        time_limit = int(request.POST['time_limit'])
        end_time = time.time() + time_limit
        request.session['end_time'] = end_time
    end_time = request.session.get('end_time')
    if end_time and end_time < time.time():
        datas = Students.objects.order_by('?').first()
        request.session['end_time'] = None

    return render(request, 'core/random.html', {'name': datas})


def students(request):
    if request.method == "POST":
        # forms = StudentForm(request.POST)
        # if forms.is_valid():
        #     students_name = forms.cleaned_data['student_name']
        #     Students.objects.create(student_name=students_name)
        #     return HttpResponseRedirect("random")
        name = request.POST['name']

        Students.objects.create(student_name=name)
        return HttpResponseRedirect("name")
    else:
        all_names = Students.objects.all()
        return render(request, "core/new_student.html", {"names": all_names})


def delete_name(request, id_name):
    name = Students.objects.get(pk=id_name)
    name.delete()
    return HttpResponseRedirect('/name')


def delete_data(request):
    Names.objects.all().delete()
    Students.objects.all().delete()
    return HttpResponseRedirect('/')

def timer(request):
    stu = request.GET.get('textt')
    names = Students.objects.filter(student_name=stu)
    names.delete()
    print(stu)
    get_time = LimitTime.objects.last()
    time_limit = get_time.timer
    end_time = time.time() + time_limit

    request.session['end_time'] = end_time
    end_time = request.session.get('end_time')

    if end_time and end_time < time.time():
        request.session['end_time'] = None
    context = {"student": stu}
    return render(request, 'core/timer.html', context)
